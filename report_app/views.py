from django.shortcuts import render
from django.db.models import Max, Sum, Subquery, OuterRef
from django.core.paginator import Paginator
from .models import LevelMetersData, Fillings
from datetime import datetime


def get_fuel_balance_data():

    latest_dates = LevelMetersData.objects.filter(
        id_level_meter=OuterRef('id_level_meter')
    ).values('id_level_meter').annotate(
        max_date=Max('date_time')
    ).values('max_date')
    
    latest_data = LevelMetersData.objects.filter(
        date_time__in=Subquery(latest_dates),
        fuel_volume_valid=True
    ).select_related('id_level_meter')
    
    total_liters = 0
    measurements = []
    for record in latest_data:
        liters = record.fuel_volume * 1000
        total_liters += liters
        measurements.append({
            'id': record.id_level_meter.id,
            'liters': int(liters),
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
