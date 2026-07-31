# limits/admin.py

from django.contrib import admin
from .models import PeriodLimit
from report_app.models import Users
from datetime import datetime, timedelta


class PeriodMonthFilter(admin.SimpleListFilter):
    title = 'Месяц периода'
    parameter_name = 'month'

    def lookups(self, request, model_admin):
        today = datetime.now().date()
        months = []
        for i in range(3):
            d = today.replace(day=1) - timedelta(days=i*30)
            months.append((d.strftime('%Y-%m'), d.strftime('%B %Y')))
        return months

    def queryset(self, request, queryset):
        if self.value():
            try:
                year, month = map(int, self.value().split('-'))
                return queryset.filter(date_from__year=year, date_from__month=month)
            except:
                return queryset
        return queryset


@admin.register(PeriodLimit)
class PeriodLimitAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'get_user_name',
        'date_from_display',
        'date_to_display',
        'period_limit',
        'new_month_limit',
        'remaining_at_period_end',
        'created_at',
    )
    list_filter = (PeriodMonthFilter,)
    search_fields = ('user_id',)
    ordering = ('-date_from',)

    def get_user_name(self, obj):
        try:
            user = Users.objects.get(id=obj.user_id)
            return user.full_name
        except Users.DoesNotExist:
            return f"⚠️ Не найден (ID: {obj.user_id})"
    get_user_name.short_description = "Техника"

    def date_from_display(self, obj):
        return obj.date_from.strftime('%d.%m.%Y')
    date_from_display.short_description = "С"

    def date_to_display(self, obj):
        return obj.date_to.strftime('%d.%m.%Y')
    date_to_display.short_description = "По"