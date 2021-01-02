from . import views
from django.urls import path

urlpatterns = [
    path('', views.dashboard, name='supervisor-dashboard'),
    path('employees/', views.employees, name='supervisor-employees'),
    path('settings/', views.settings, name='supervisor-settings'),
    path('vehicles/', views.vehicles, name='supervisor-vehicles'),
]
