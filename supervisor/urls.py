from . import views
from .views import (VehicleListsView, VehicleDeleteView,EmployeeDeleteView, EmployeesListsView, EmployeeDetailsView, ToursListsView, TourDeleteView, TourDetailsView)
from django.urls import path

urlpatterns = [
    #Admin settings
    path('', views.dashboard, name='supervisor-dashboard'),
    path('validate_username/', views.validate_username, name='validate_username'),
    path('validate_plate/', views.validate_plate, name='validate_plate'),

    #Vehicles
    path('vehicles/', VehicleListsView.as_view(), name='supervisor-vehicles-list'),
    path('vehicles/add', views.vehicle_add, name='supervisor-vehicle-add'),
    path('vehicles/<int:pk>/delete/', VehicleDeleteView.as_view(template_name='supervisor/vehicle_confirm_delete.html'), name='supervisor-vehicle-delete'),

    #Employees
    path('employees/', EmployeesListsView.as_view(), name='supervisor-employees-list'),
    path('employees/<int:pk>/', EmployeeDetailsView.as_view(template_name='supervisor/employee_details.html'), name='supervisor-employees-details'),
    path('employees/add', views.employee_add, name='supervisor-employees-add'),
    path('employees/<int:pk>/delete/', EmployeeDeleteView.as_view(template_name='supervisor/user_confirm_delete.html'), name='supervisor-employee-delete'),

    #Tours
    path('tours/', ToursListsView.as_view(), name='supervisor-tours-list'),
    path('tours/<int:pk>/delete/', TourDeleteView.as_view(), name='supervisor-tour-delete'),
    path('tours/<int:pk>/', TourDetailsView.as_view(template_name='supervisor/tour_detail.html'), name='supervisor-tour-details'),

]
