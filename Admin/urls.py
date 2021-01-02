from . import views
from django.urls import path

urlpatterns = [
    path('', views.dashboard, name='admin-dashboard'),
    path('employees/', views.employees, name='admin-employees'),
    path('settings/', views.settings, name='admin-settings'),
    path('vehicles/', views.vehicles, name='admin-vehicles'),
]
