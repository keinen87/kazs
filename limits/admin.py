# limits/admin.py

from django.contrib import admin
from .models import WeekLimit

@admin.register(WeekLimit)
class WeekLimitAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'week_start', 'week_end', 'weekly_limit', 'new_month_limit', 'created_at')
    search_fields = ('user_id',)
    list_filter = ('week_start',)
    ordering = ('-week_start',)