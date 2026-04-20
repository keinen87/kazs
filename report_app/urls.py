from django.urls import path
from . import views

app_name = 'report_app'

urlpatterns = [
    path('fillings/', views.fillings_list, name='fillings_list'),
]