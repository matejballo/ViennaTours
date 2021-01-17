from . import views
from .views import (VehicleListsView, VehicleDeleteView)
from django.urls import path

urlpatterns = [
    #Admin settings
    path('', views.dashboard, name='supervisor-dashboard'),
    path('settings/', views.settings, name='supervisor-settings'),
    path('validate_username/', views.validate_username, name='validate_username'),
    path('validate_plate/', views.validate_plate, name='validate_plate'),

    #Vehicles
    path('vehicles/', VehicleListsView.as_view(), name='supervisor-vehicles-list'),
    path('vehicles/add', views.vehicle_add, name='supervisor-vehicle-add'),
    path('vehicles/<int:pk>/delete/', VehicleDeleteView.as_view(template_name='supervisor/vehicle_confirm_delete.html'), name='supervisor-vehicle-delete'),

    #Employees
    path('employees/', views.employees_list, name='supervisor-employees-list'),
    path('employees/add', views.employee_add, name='supervisor-employees-add'),
    path('employees/<int:pk>/delete/', VehicleDeleteView.as_view(template_name='supervisor/vehicle_confirm_delete.html'), name='supervisor-vehicle-delete'),

    #Tours
    path('tours/', views.tours_list, name='supervisor-tours-list'),
    path('tours/<int:pk>/delete/', views.tours_list, name='supervisor-tours-delete'),
]
