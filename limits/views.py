from django.shortcuts import render
from django.db.models import Sum
from django.http import JsonResponse, FileResponse
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from datetime import datetime, timedelta
from report_app.models import Users, Fillings
from report_app.views import datetime_to_ticks, SKIP_USER_IDS
from .models import PeriodLimit
import json
import io


MONTH_NAMES = {
    1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель',
    5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
    9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
}


def get_month_start(date):
    if isinstance(date, datetime):
        date = date.date()
    return datetime(date.year, date.month, 1).date()


def date_to_datetime(d, hour=0, minute=0, second=0):
    return datetime(d.year, d.month, d.day, hour, minute, second)


def limits_page(request):
    today = datetime.now().date()
    date_from_str = request.GET.get('date_from')
    date_to_str = request.GET.get('date_to')
    
    if date_from_str and date_to_str:
        try:
            date_from = datetime.strptime(date_from_str, '%Y-%m-%d').date()
            date_to = datetime.strptime(date_to_str, '%Y-%m-%d').date()
        except ValueError:
            date_from = get_month_start(today)
            date_to = today
    else:
        date_from = get_month_start(today)
        date_to = today

    is_same_month = (date_from.year == date_to.year and date_from.month == date_to.month)
    is_past_period = date_to < today
    is_editable = not is_past_period and is_same_month

    users = Users.objects.exclude(id__in=SKIP_USER_IDS).order_by('full_name')

    month_start = get_month_start(today)
    ticks_month_start = datetime_to_ticks(date_to_datetime(month_start, 0, 0, 0))
    ticks_today = datetime_to_ticks(now())

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

    period_limits = {
        pl.user_id: pl
        for pl in PeriodLimit.objects.filter(date_from=date_from, date_to=date_to)
    }

    data = []
    for user in users:
        base_limit = user.month_limit if user.month_limit is not None else 0.0
        spent_month = expenses_month.get(user.id, 0)
        remaining_month = base_limit - spent_month if base_limit is not None else None

        pl = period_limits.get(user.id)
        if pl:
            period_limit = pl.period_limit
            new_month_limit = pl.new_month_limit
            remaining_at_period_end = pl.remaining_at_period_end
        else:
            period_limit = None
            new_month_limit = None
            remaining_at_period_end = None

        data.append({
            'user': user,
            'base_limit': base_limit,
            'remaining_month': remaining_month,
            'period_limit': period_limit,
            'new_month_limit': new_month_limit,
            'remaining_at_period_end': remaining_at_period_end,
        })

    context = {
        'data': data,
        'date_from': date_from,
        'date_to': date_to,
        'now': now(),
        'is_editable': is_editable,
        'is_past_period': is_past_period,
        'month_name': MONTH_NAMES.get(date_from.month, ''),
    }
    return render(request, 'limits.html', context)


@login_required
def save_period_limit(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    try:
        body = json.loads(request.body)
        user_id = body.get('user_id')
        date_from_str = body.get('date_from')
        date_to_str = body.get('date_to')
        period_limit = body.get('period_limit')
        remaining_month = body.get('remaining_month')
        if user_id is None or date_from_str is None or date_to_str is None or period_limit is None or remaining_month is None:
            return JsonResponse({'status': 'error', 'message': 'Missing fields'}, status=400)

        date_from = datetime.strptime(date_from_str, '%Y-%m-%d').date()
        date_to = datetime.strptime(date_to_str, '%Y-%m-%d').date()
        user = Users.objects.get(id=user_id)

        base_limit = user.month_limit or 0.0
        period_limit = float(period_limit)
        remaining_month = float(remaining_month)

        prev_period = PeriodLimit.objects.filter(
            user_id=user_id,
            date_to__lt=date_from,
            date_from__year=date_from.year,
            date_from__month=date_from.month
        ).order_by('-date_to').first()

        if prev_period:
            prev_cumulative = float(prev_period.new_month_limit or base_limit)
            prev_remaining = float(prev_period.remaining_at_period_end or 0)
            burned = max(0, prev_remaining)
            cumulative = prev_cumulative + period_limit - burned
        else:
            burned = max(0, remaining_month)
            cumulative = base_limit + period_limit - burned

        period_limit_obj, created = PeriodLimit.objects.get_or_create(
            user_id=user_id,
            date_from=date_from,
            date_to=date_to,
            defaults={
                'period_limit': period_limit,
                'new_month_limit': cumulative,
                'remaining_at_period_end': remaining_month,
            }
        )
        if not created:
            period_limit_obj.period_limit = period_limit
            period_limit_obj.new_month_limit = cumulative
            period_limit_obj.remaining_at_period_end = remaining_month
            period_limit_obj.save()

        return JsonResponse({
            'status': 'ok',
            'new_month_limit': cumulative,
            'period_limit': period_limit,
            'remaining_at_period_end': remaining_month,
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
            date_from_str = row.get('date_from')
            date_to_str = row.get('date_to')
            period_limit = row.get('period_limit')
            remaining_month = row.get('remaining_month')
            if user_id is None or date_from_str is None or date_to_str is None or remaining_month is None:
                continue

            if period_limit is None or period_limit == '' or float(period_limit) <= 0:
                is_auto = True
                period_limit = 1.0
            else:
                period_limit = float(period_limit)
                is_auto = False

            try:
                date_from = datetime.strptime(date_from_str, '%Y-%m-%d').date()
                date_to = datetime.strptime(date_to_str, '%Y-%m-%d').date()
            except ValueError:
                continue
            user = Users.objects.get(id=user_id)

            base_limit = user.month_limit or 0.0
            remaining_month = float(remaining_month)

            if is_auto:
                if base_limit == 1:
                    cumulative = 1.0
                else:
                    cumulative = base_limit + 1.0
            else:
                prev_period = PeriodLimit.objects.filter(
                    user_id=user_id,
                    date_to__lt=date_from,
                    date_from__year=date_from.year,
                    date_from__month=date_from.month
                ).order_by('-date_to').first()
                if prev_period:
                    prev_cumulative = float(prev_period.new_month_limit or base_limit)
                    prev_remaining = float(prev_period.remaining_at_period_end or 0)
                    burned = max(0, prev_remaining)
                    cumulative = prev_cumulative + period_limit - burned
                else:
                    burned = max(0, remaining_month)
                    cumulative = base_limit + period_limit - burned

            period_limit_obj, created = PeriodLimit.objects.get_or_create(
                user_id=user_id,
                date_from=date_from,
                date_to=date_to,
                defaults={
                    'period_limit': period_limit,
                    'new_month_limit': cumulative,
                    'remaining_at_period_end': remaining_month,
                }
            )
            if not created:
                period_limit_obj.period_limit = period_limit
                period_limit_obj.new_month_limit = cumulative
                period_limit_obj.remaining_at_period_end = remaining_month
                period_limit_obj.save()
            updated.append(user_id)

        return JsonResponse({'status': 'ok', 'updated': updated})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@login_required
def backup_limits(request):
    if request.method != 'GET':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    users = Users.objects.exclude(id__in=SKIP_USER_IDS).order_by('full_name')

    data = []
    for user in users:
        data.append({
            'user_id': user.id,
            'user_name': user.full_name,
            'month_limit': float(user.month_limit) if user.month_limit is not None else None,
        })

    json_data = {
        'exported_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'data': data
    }

    json_str = json.dumps(json_data, ensure_ascii=False, indent=2)
    filename = f"limits_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
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
        date_from_str = body.get('date_from')
        date_to_str = body.get('date_to')
        if not date_from_str or not date_to_str:
            return JsonResponse({'status': 'error', 'message': 'Missing dates'}, status=400)

        date_from = datetime.strptime(date_from_str, '%Y-%m-%d').date()
        date_to = datetime.strptime(date_to_str, '%Y-%m-%d').date()

        period_limits = PeriodLimit.objects.filter(date_from=date_from, date_to=date_to)
        if not period_limits.exists():
            return JsonResponse({'status': 'error', 'message': 'No limits found for this period'}, status=400)

        updated_count = 0
        for pl in period_limits:
            # Пропускаем пользователей из SKIP_USER_IDS
            if pl.user_id in SKIP_USER_IDS:
                continue
            user = Users.objects.filter(id=pl.user_id).first()
            if user and pl.new_month_limit is not None:
                user.month_limit = pl.new_month_limit
                user.save(using='default')
                updated_count += 1

        return JsonResponse({'status': 'ok', 'updated': updated_count})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)