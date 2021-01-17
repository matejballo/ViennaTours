from . import views
from django.urls import path

urlpatterns = [
    path('', views.dashboard, name='supervisor-dashboard'),
  
    path('settings/', views.settings, name='supervisor-settings'),

    path('cars/', views.vehicles, name='supervisor-cars'),
    path('cars/add', views.createcar, name='supervisor-cars-add'),
    path('cars/<int:pk>/delete/', views.createcar, name='supervisor-cars-delete'),

    path('employees/', views.employees, name='supervisor-employees'),
    path('employees/add', views.registration, name='supervisor-registration'),
    path('tours/', views.listdata, name='supervisor-listdata'),
    path('tours/<int:pk>/delete/', views.listdata, name='supervisor-listdata'),
    path('validate_username/', views.validate_username, name='validate_username')
]
