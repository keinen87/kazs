# limits/urls.py

from django.urls import path
from . import views

app_name = 'limits'

urlpatterns = [
    path('', views.limits_page, name='limits_page'),
    path('save-weekly-limit/', views.save_weekly_limit, name='save_weekly_limit'),
    path('save-all-limits/', views.save_all_limits, name='save_all_limits'),
    path('backup-limits/', views.backup_limits, name='backup_limits'),
    path('sync-limits-to-postgres/', views.sync_limits_to_postgres, name='sync_limits_to_postgres'),
]