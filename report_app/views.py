from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import JsonResponse
from .models import LevelMetersData, Fillings, Users
from datetime import datetime


# ---------------------- Вспомогательные функции ----------------------
def ticks_to_datetime(ticks):
    """Преобразует .NET ticks в datetime object"""
    if not ticks or ticks <= 0:
        return None
    try:
        epoch_ticks = 621355968000000000
        seconds = (ticks - epoch_ticks) / 10_000_000
        return datetime.fromtimestamp(seconds)
    except (ValueError, OverflowError, OSError):
        return None


def datetime_to_ticks(dt):
    """Преобразует datetime object в .NET ticks"""
    epoch_ticks = 621355968000000000
    seconds = dt.timestamp()
    return int(seconds * 10_000_000 + epoch_ticks)


# ---------------------- Константы ----------------------
SKIP_USER_IDS = {3, 4, 5, 6}          # пользователи без лимитов (операторы, приём топлива)
LIMIT_START_DATE = datetime(2026, 5, 5)  # с этой даты начинаем показывать лимиты и остатки


# ---------------------- Данные по уровнемерам (общие) ----------------------
def get_fuel_balance_data():
    desired_ids = [1, 2, 3, 4]
    measurements = []
    total_liters = 0

    for lm_id in desired_ids:
        latest = LevelMetersData.objects.filter(
            id_level_meter_id=lm_id,
            fuel_volume_valid=True
        ).order_by('-date_time').first()

        if latest:
            liters = latest.fuel_volume * 1000
            total_liters += liters
            level_cm = None
            if latest.level is not None and latest.level_valid:
                level_cm = float(latest.level) * 100
            measurements.append({
                'id': lm_id,
                'liters': int(liters),
                'level_cm': level_cm,
            })
        else:
            measurements.append({
                'id': lm_id,
                'liters': None,
                'level_cm': None,
            })

    return {
        'total_volume': int(total_liters),
        'measurements': measurements,
    }


def fuel_balance_api(request):
    """Возвращает JSON с остатками топлива для AJAX-обновления"""
    data = get_fuel_balance_data()
    return JsonResponse(data)


# ---------------------- Основная страница со списком заправок ----------------------
def fillings_list(request):
    balance_data = get_fuel_balance_data()
    search_query = request.GET.get('search', '').strip()

    # Базовый запрос заправок (только положительные литры)
    fillings = Fillings.objects.select_related(
        'id_user', 'id_controller', 'id_car', 'id_fuel'
    ).filter(litre__gt=0)

    if search_query:
        fillings = fillings.filter(id_user__full_name__icontains=search_query)

    fillings = fillings.order_by('-date_time')  # от новых к старым

    now = datetime.now()
    month_start = datetime(now.year, now.month, 1)
    ticks_month_start = datetime_to_ticks(month_start)

    # Преобразуем даты и проставляем лимит пользователя (кроме исключённых)
    for filling in fillings:
        filling.dt = ticks_to_datetime(filling.date_time)
        user = filling.id_user
        if user and user.id not in SKIP_USER_IDS:
            filling.month_limit = user.month_limit
        else:
            filling.month_limit = None

    # Расчёт остатка на момент заправки (только для заправок после LIMIT_START_DATE)
    for filling in fillings:
        user = filling.id_user
        # Для заправок раньше 5 мая 2026 – скрываем и лимит, и остаток
        if filling.dt and filling.dt < LIMIT_START_DATE:
            filling.month_limit = None
            filling.remaining = None
            continue

        if (user and user.id not in SKIP_USER_IDS and filling.month_limit is not None):
            spent_up_to_date = Fillings.objects.filter(
                id_user=user,
                litre__gt=0,
                date_time__gte=ticks_month_start,
                date_time__lte=filling.date_time
            ).aggregate(total=Sum('litre'))['total'] or 0
            filling.remaining = filling.month_limit - spent_up_to_date
        else:
            filling.remaining = None

    # Пагинация
    paginator = Paginator(fillings, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'total_volume': balance_data['total_volume'],
        'measurements': balance_data['measurements'],
        'search_query': search_query,
    }
    return render(request, 'fillings_list.html', context)


# ---------------------- Отчёт по выдаче топлива ----------------------
def fuel_report(request):
    # Показываем только тех пользователей, у которых есть хотя бы одна заправка
    users = Users.objects.filter(
        id__in=Fillings.objects.filter(litre__gt=0).values('id_user').distinct()
    ).order_by('full_name')

    selected_user_id = request.GET.get('user_id')
    date_from_str = request.GET.get('date_from')
    date_to_str = request.GET.get('date_to')
    
    total_litres = None
    selected_user = None
    remaining = None
    error = None

    if selected_user_id and date_from_str and date_to_str:
        try:
            selected_user = Users.objects.get(id=selected_user_id)
            date_from = datetime.strptime(date_from_str, '%Y-%m-%d')
            date_to = datetime.strptime(date_to_str, '%Y-%m-%d')
            date_to_end = datetime(date_to.year, date_to.month, date_to.day, 23, 59, 59)
            
            ticks_from = datetime_to_ticks(date_from)
            ticks_to = datetime_to_ticks(date_to_end)
            
            total = Fillings.objects.filter(
                id_user=selected_user,
                litre__gt=0,
                date_time__gte=ticks_from,
                date_time__lte=ticks_to
            ).aggregate(total=Sum('litre'))['total']
            
            total_litres = total if total is not None else 0

            # Для служебных пользователей лимит и остаток не показываем
            if selected_user.id not in SKIP_USER_IDS:
                if selected_user.month_limit is not None:
                    remaining = selected_user.month_limit - total_litres
                else:
                    remaining = None
            else:
                remaining = None
                selected_user.month_limit = None

        except Users.DoesNotExist:
            error = "Выбранная машина не найдена"
        except Exception as e:
            error = f"Ошибка: {str(e)}"
    
    context = {
        'users': users,
        'selected_user_id': selected_user_id,
        'selected_user': selected_user,
        'date_from': date_from_str,
        'date_to': date_to_str,
        'total_litres': total_litres,
        'remaining': remaining,
        'error': error,
    }
    return render(request, 'fuel_report.html', context)