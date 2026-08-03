from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import JsonResponse
from django.conf import settings   # <--- добавлен импорт
from .models import LevelMetersData, Fillings, Users
from datetime import datetime, timedelta
from calendar import monthrange
import requests
import memcache
import subprocess
import platform

# ---------------------- Константы FortMonitor ----------------------
FM_REPORT_URL = "http://31.173.168.107:8080/"
FM_URL_TEMPLATE = "http://31.173.168.107:8080/api/integration/v1/"
FM_LOGIN = "bassol_api"
FM_PASSWORD = "Bassl22052026"
FM_MC_SERVER = '127.0.0.1:11211'
FM_CACHE_TIMEOUT = 300   # 5 минут

VEHICLE_MAP = {
    '8': 'Hino',
    '9': 'Hitachi 1',
    '10': 'Hitachi 2',
    '24': 'Rimpull 1',
    '23': 'Rimpull 2',
    '25': 'Rimpull 3',
    '22': 'Vermeer 1',
    '15': 'Автокран XCMG',
    '16': 'Кран Zoomlion',
    '18': 'Камаз 65201',
    '21': 'Автопогрузчик FH',
    '29': 'Погрузчик Lonkin',
    '26': 'Подборщик',
    '32': 'Тепловоз ТЭМ7А',
    '31': 'Тепловоз ТЭМ9'
}

# ---------------------- Константы приложения ----------------------
SKIP_USER_IDS = {0, 1, 2, 3, 4, 5, 6, 39}
LIMIT_START_DATE = datetime(2026, 5, 5)
# KAZS_IP теперь читается из settings


# ---------------------- Вспомогательные функции ----------------------
def ticks_to_datetime(ticks):
    if not ticks or ticks <= 0:
        return None
    try:
        epoch_ticks = 621355968000000000
        seconds = (ticks - epoch_ticks) / 10_000_000
        return datetime.fromtimestamp(seconds)
    except (ValueError, OverflowError, OSError):
        return None


def datetime_to_ticks(dt):
    epoch_ticks = 621355968000000000
    seconds = dt.timestamp()
    return int(seconds * 10_000_000 + epoch_ticks)


def check_kazs_online():
    """Проверяет доступность КАЗС по IP из настроек с кэшированием в memcached (30 секунд)"""
    mc = memcache.Client([FM_MC_SERVER], debug=0)
    cache_key = "kazs_status"
    cached = mc.get(cache_key)
    if cached is not None:
        return cached

    ip = settings.KAZS_IP   # используем значение из настроек
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", ip]
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=2)
        online = result.returncode == 0
    except (subprocess.TimeoutExpired, Exception):
        online = False

    mc.set(cache_key, online, time=30)
    return online

# ... остальные функции (get_session_id, get_valid_session, ...) без изменений ...