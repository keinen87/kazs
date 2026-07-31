# limits/views.py

from django.shortcuts import render
from django.db.models import Sum
from django.http import JsonResponse, FileResponse
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from datetime import datetime, timedelta
from report_app.models import Users, Fillings
from report_app.views import datetime_to_ticks, SKIP_USER_IDS
from .models import WeekLimit
import json
import io


MONTH_NAMES = {
    1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель',
    5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
    9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
}


def get_monday(date):
    if isinstance(date, datetime):
        date = date.date()
    return date - timedelta(days=date.weekday())


def get_month_start(date):
    if isinstance(date, datetime):
        date = date.date()
    return datetime(date.year, date.month, 1).date()


def get_week_end(week_start):
    if isinstance(week_start, datetime):
        week_start = week_start.date()
    return week_start + timedelta(days=6)


def date_to_datetime(d, hour=0, minute=0, second=0):
    return datetime(d.year, d.month, d.day, hour, minute, second)


def limits_page(request):
    today = datetime.now().date()
    week_start_str = request.GET.get('week_start')
    if week_start_str:
        try:
            selected_date = datetime.strptime(week_start_str, '%Y-%m-%d').date()
            week_start = get_monday(selected_date)
        except ValueError:
            week_start = get_monday(today)
    else:
        week_start = get_monday(today)

    week_end = get_week_end(week_start)
    current_monday = get_monday(today)
    is_past_week = week_start < current_monday
    month_name = MONTH_NAMES.get(week_start.month, '')

    users = Users.objects.exclude(id__in=SKIP_USER_IDS).order_by('full_name')

    month_start = get_month_start(today)
    ticks_month_start = datetime_to_ticks(date_to_datetime(month_start, 0, 0, 0))
    ticks_today = datetime_to_ticks(now())

    # Расход за месяц
    expenses_month = {}
    if users.exists():
        expense_qs = Fillings.objects.filter(
            id_user__in=users,
            litre__gt=0,
            date_time__gte=ticks_month_start,
            date_time__lte=ticks_today,
            date_time__isnull=False,
            date_time__gt=0
        ).values('id_user').annotate(total=Sum('litre'))
        for item in expense_qs:
            expenses_month[item['id_user']] = float(item['total'])

    # Загружаем сохранённые недельные лимиты
    week_limits = {
        wl.user_id: wl
        for wl in WeekLimit.objects.filter(week_start=week_start)
    }

    data = []
    for user in users:
        base_limit = user.month_limit if user.month_limit is not None else 0.0
        spent_month = expenses_month.get(user.id, 0)
        remaining_month = base_limit - spent_month if base_limit is not None else None

        wl = week_limits.get(user.id)
        if wl:
            weekly_limit = wl.weekly_limit
            new_month_limit = wl.new_month_limit
            week_remaining = wl.week_remaining
        else:
            weekly_limit = None
            new_month_limit = None
            week_remaining = None

        data.append({
            'user': user,
            'base_limit': base_limit,
            'remaining_month': remaining_month,
            'weekly_limit': weekly_limit,
            'new_month_limit': new_month_limit,
            'week_remaining': week_remaining,
        })

    context = {
        'data': data,
        'week_start': week_start,
        'week_end': week_end,
        'now': now(),
        'is_past_week': is_past_week,
        'month_name': month_name,
    }
    return render(request, 'limits.html', context)


@login_required
def save_weekly_limit(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    try:
        body = json.loads(request.body)
        user_id = body.get('user_id')
        week_start_str = body.get('week_start')
        weekly_limit = body.get('weekly_limit')
        week_remaining = body.get('week_remaining')
        if user_id is None or week_start_str is None or weekly_limit is None or week_remaining is None:
            return JsonResponse({'status': 'error', 'message': 'Missing fields'}, status=400)

        selected_date = datetime.strptime(week_start_str, '%Y-%m-%d').date()
        week_start = get_monday(selected_date)
        week_end = get_week_end(week_start)
        user = Users.objects.get(id=user_id)

        base_limit = user.month_limit or 0.0
        weekly_limit = float(weekly_limit)
        week_remaining_current = float(week_remaining)

        prev_week = WeekLimit.objects.filter(
            user_id=user_id,
            week_start__lt=week_start,
            week_start__year=week_start.year,
            week_start__month=week_start.month
        ).order_by('-week_start').first()

        if prev_week:
            prev_cumulative = float(prev_week.new_month_limit or base_limit)
            prev_remaining = float(prev_week.week_remaining or 0)
            burned = max(0, prev_remaining)
            cumulative = prev_cumulative + weekly_limit - burned
        else:
            burned = max(0, week_remaining_current)
            cumulative = base_limit + weekly_limit - burned

        week_limit_obj, created = WeekLimit.objects.get_or_create(
            user_id=user_id,
            week_start=week_start,
            defaults={
                'week_end': week_end,
                'weekly_limit': weekly_limit,
                'new_month_limit': cumulative,
                'week_remaining': week_remaining_current,
            }
        )
        if not created:
            week_limit_obj.weekly_limit = weekly_limit
            week_limit_obj.new_month_limit = cumulative
            week_limit_obj.week_remaining = week_remaining_current
            week_limit_obj.save()

        return JsonResponse({
            'status': 'ok',
            'new_month_limit': cumulative,
            'weekly_limit': weekly_limit,
            'week_remaining': week_remaining_current,
            'week_start': week_start.strftime('%Y-%m-%d'),
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@login_required
def save_all_limits(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    try:
        body = json.loads(request.body)
        rows = body.get('rows', [])
        if not rows:
            return JsonResponse({'status': 'error', 'message': 'No data'}, status=400)

        updated = []
        for row in rows:
            user_id = row.get('user_id')
            week_start_str = row.get('week_start')
            weekly_limit = row.get('weekly_limit')
            week_remaining = row.get('week_remaining')
            if user_id is None or week_start_str is None or week_remaining is None:
                continue

            # Определяем, задан ли недельный лимит
            if weekly_limit is None or weekly_limit == '' or float(weekly_limit) <= 0:
                is_auto = True
                # weekly_limit сохраняем как 1 для базы (но не используется в расчёте)
                weekly_limit = 1.0
            else:
                weekly_limit = float(weekly_limit)
                is_auto = False

            try:
                selected_date = datetime.strptime(week_start_str, '%Y-%m-%d').date()
                week_start = get_monday(selected_date)
            except ValueError:
                continue
            week_end = get_week_end(week_start)
            user = Users.objects.get(id=user_id)

            base_limit = user.month_limit or 0.0
            week_remaining_current = float(week_remaining)

            prev_week = WeekLimit.objects.filter(
                user_id=user_id,
                week_start__lt=week_start,
                week_start__year=week_start.year,
                week_start__month=week_start.month
            ).order_by('-week_start').first()

            if is_auto:
                # Лимит не задан: новый = base_limit + 1 (но если base_limit == 1, оставляем 1)
                if base_limit == 1:
                    cumulative = 1.0
                else:
                    cumulative = base_limit + 1.0
            else:
                if prev_week:
                    prev_cumulative = float(prev_week.new_month_limit or base_limit)
                    prev_remaining = float(prev_week.week_remaining or 0)
                    burned = max(0, prev_remaining)
                    cumulative = prev_cumulative + weekly_limit - burned
                else:
                    burned = max(0, week_remaining_current)
                    cumulative = base_limit + weekly_limit - burned

            week_limit_obj, created = WeekLimit.objects.get_or_create(
                user_id=user_id,
                week_start=week_start,
                defaults={
                    'week_end': week_end,
                    'weekly_limit': weekly_limit,
                    'new_month_limit': cumulative,
                    'week_remaining': week_remaining_current,
                }
            )
            if not created:
                week_limit_obj.weekly_limit = weekly_limit
                week_limit_obj.new_month_limit = cumulative
                week_limit_obj.week_remaining = week_remaining_current
                week_limit_obj.save()
            updated.append(user_id)

        return JsonResponse({'status': 'ok', 'updated': updated})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@login_required
def backup_limits(request):
    if request.method != 'GET':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    week_start_str = request.GET.get('week_start')
    if not week_start_str:
        return JsonResponse({'status': 'error', 'message': 'Missing week_start'}, status=400)

    try:
        selected_date = datetime.strptime(week_start_str, '%Y-%m-%d').date()
        week_start = get_monday(selected_date)
    except ValueError:
        return JsonResponse({'status': 'error', 'message': 'Invalid date'}, status=400)

    week_limits = WeekLimit.objects.filter(week_start=week_start)
    data = []
    for wl in week_limits:
        user = Users.objects.filter(id=wl.user_id).first()
        if user:
            data.append({
                'user_id': user.id,
                'user_name': user.full_name,
                'month_limit': wl.new_month_limit,
            })

    json_data = {
        'week_start': week_start.strftime('%Y-%m-%d'),
        'exported_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'data': data
    }

    json_str = json.dumps(json_data, ensure_ascii=False, indent=2)
    filename = f"limits_backup_{week_start.strftime('%Y%m%d')}.json"
    response = FileResponse(
        io.BytesIO(json_str.encode('utf-8')),
        content_type='application/json',
        as_attachment=True,
        filename=filename
    )
    return response


@login_required
def sync_limits_to_postgres(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    try:
        body = json.loads(request.body)
        week_start_str = body.get('week_start')
        if not week_start_str:
            return JsonResponse({'status': 'error', 'message': 'Missing week_start'}, status=400)

        try:
            selected_date = datetime.strptime(week_start_str, '%Y-%m-%d').date()
            week_start = get_monday(selected_date)
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid date format'}, status=400)

        week_limits = WeekLimit.objects.filter(week_start=week_start)
        if not week_limits.exists():
            return JsonResponse({'status': 'error', 'message': 'No limits found for this week'}, status=400)

        updated_count = 0
        for wl in week_limits:
            user = Users.objects.filter(id=wl.user_id).first()
            if user and wl.new_month_limit is not None:
                user.month_limit = wl.new_month_limit
                user.save(using='default')
                updated_count += 1

        return JsonResponse({'status': 'ok', 'updated': updated_count})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)