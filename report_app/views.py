from django.shortcuts import render
from django.db.models import Max, Sum, Subquery, OuterRef
from django.core.paginator import Paginator
from .models import LevelMetersData, Fillings
from datetime import datetime


def get_fuel_balance_data():
    desired_ids = [1, 2, 3, 4]  # ID уровнемеров, которые нужно показать
    measurements = []
    total_liters = 0

    for lm_id in desired_ids:
        # Последняя запись с валидным fuel_volume для данного уровнемера
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
            # Нет данных – показываем прочерки
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
    """Преобразует .NET ticks в datetime object"""
    if not ticks or ticks <= 0:
        return None
    try:
        epoch_ticks = 621355968000000000
        seconds = (ticks - epoch_ticks) / 10_000_000
        return datetime.fromtimestamp(seconds)
    except (ValueError, OverflowError, OSError):
        return None


def fillings_list(request):
    # Получаем данные об остатках топлива
    balance_data = get_fuel_balance_data()
    
    # Основной запрос заправок (исключаем нулевые литры)
    fillings = Fillings.objects.select_related(
        'id_user', 'id_controller', 'id_car', 'id_fuel'
    ).filter(litre__gt=0).order_by('-date_time')   # ← добавлен фильтр
    
    for filling in fillings:
        filling.dt = ticks_to_datetime(filling.date_time)
    
    paginator = Paginator(fillings, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_volume': balance_data['total_volume'],
        'measurements': balance_data['measurements'],
    }
    return render(request, 'fillings_list.html', context)
