from . import views
from django.urls import path

urlpatterns = [
    path('', views.dashboard, name='supervisor-dashboard'),
    path('employees/', views.employees, name='supervisor-employees'),
    path('settings/', views.settings, name='supervisor-settings'),
    path('vehicles/', views.vehicles, name='supervisor-vehicles'),
    path('listdata/', views.listdata, name='supervisor-listdata'),
    path('listcar/', views.listcar, name='supervisor-listcar'),
    path('createcar/', views.createcar, name='supervisor-car'),
    path('registration/', views.registration, name='supervisor-registration'),
]
