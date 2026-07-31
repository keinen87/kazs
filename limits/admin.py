# limits/admin.py

from django.contrib import admin
from .models import WeekLimit
from report_app.models import Users

@admin.register(WeekLimit)
class WeekLimitAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'get_user_name',
        'week_start',
        'week_end',
        'weekly_limit',
        'new_month_limit',
        'week_remaining',
        'created_at',
    )
    list_filter = ('week_start',)
    search_fields = ('user_id',)  # поиск по ID техники
    ordering = ('-week_start',)

    def get_user_name(self, obj):
        try:
            user = Users.objects.get(id=obj.user_id)
            return user.full_name
        except Users.DoesNotExist:
            return f"⚠️ Не найден (ID: {obj.user_id})"
    get_user_name.short_description = "Техника"