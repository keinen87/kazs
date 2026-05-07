from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.http import JsonResponse
from .models import LevelMetersData, Fillings, Users
from datetime import datetime


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


def ticks_to_datetime(ticks):
    if not ticks or ticks <= 0:
        return None
    try:
        epoch_ticks = 621355968000000000
        seconds = (ticks - epoch_ticks) / 10_000_000
        return datetime.fromtimestamp(seconds)
    except (ValueError, OverflowError, OSError):
        return None


def fillings_list(request):
    balance_data = get_fuel_balance_data()

    SKIP_USER_IDS = {3, 4, 5, 6}  # пользователи без лимитов

    search_query = request.GET.get('search', '').strip()

    fillings = Fillings.objects.select_related(
        'id_user', 'id_controller', 'id_car', 'id_fuel'
    ).filter(litre__gt=0)

    if search_query:
        fillings = fillings.filter(id_user__full_name__icontains=search_query)

    fillings = fillings.order_by('-date_time')

    now = datetime.now()
    month_start = datetime(now.year, now.month, 1)

    spent_dict = {}
    for filling in fillings:
        filling.dt = ticks_to_datetime(filling.date_time)

        user = filling.id_user
        if user and user.id not in SKIP_USER_IDS:
            filling.month_limit = user.month_limit
            if filling.dt and filling.dt >= month_start:
                spent_dict[user.id] = spent_dict.get(user.id, 0) + filling.litre
        else:
            filling.month_limit = None

    for filling in fillings:
        if filling.id_user and filling.id_user.id not in SKIP_USER_IDS:
            limit = filling.month_limit or 0
            spent = spent_dict.get(filling.id_user.id, 0)
            filling.remaining = limit - spent
        else:
            filling.remaining = None

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


def fuel_report(request):

    # Пользователи, у которых есть хотя бы одна заправка
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
            
            def datetime_to_ticks(dt):
                epoch_ticks = 621355968000000000
                seconds = dt.timestamp()
                return int(seconds * 10_000_000 + epoch_ticks)
            
            ticks_from = datetime_to_ticks(date_from)
            ticks_to = datetime_to_ticks(date_to_end)
            
            total = Fillings.objects.filter(
                id_user=selected_user,
                litre__gt=0,
                date_time__gte=ticks_from,
                date_time__lte=ticks_to
            ).aggregate(total=Sum('litre'))['total']
            
            total_litres = total if total is not None else 0
            
            # Расчёт остатка по лимиту (только если лимит задан)
            if selected_user.month_limit is not None:
                remaining = selected_user.month_limit - total_litres
            else:
                remaining = None
                
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