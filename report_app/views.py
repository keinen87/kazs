from django.shortcuts import render
from django.core.paginator import Paginator
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

    # ID пользователей, для которых не показываем лимит и остаток
    SKIP_USER_IDS = {3, 4, 5, 6}

    fillings = Fillings.objects.select_related(
        'id_user', 'id_controller', 'id_car', 'id_fuel'
    ).filter(litre__gt=0).order_by('-date_time')

    now = datetime.now()
    month_start = datetime(now.year, now.month, 1)

    # Словарь расхода за месяц только для обычных пользователей (не из SKIP)
    spent_dict = {}
    for filling in fillings:
        filling.dt = ticks_to_datetime(filling.date_time)

        user = filling.id_user
        if user and user.id not in SKIP_USER_IDS:
            filling.month_limit = user.month_limit
            if filling.dt and filling.dt >= month_start:
                spent_dict[user.id] = spent_dict.get(user.id, 0) + filling.litre
        else:
            filling.month_limit = None  # для пропущенных пользователей

    # Добавляем остаток для каждой заправки
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
    }
    return render(request, 'fillings_list.html', context)