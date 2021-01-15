from . import views
from .views import (TourListsView, TourDetailView, TourCreateView, TourUpdateView, TourDeleteView)
from django.urls import path

urlpatterns = [
    path('', views.dashboard, name='user-dashboard'),
    path('settings/', views.settings, name='user-settings'),
    path('profile/', views.profile, name='user-profile'),
    path('tours/', TourListsView.as_view(), name='user-tours'),
    path('tours/add/', TourCreateView.as_view(template_name='users/tour_form.html'), name='tour-new'),
    path('tours/<int:pk>/update/', TourUpdateView.as_view(template_name='users/tour_form.html'), name='tour-update'),
    path('tours/<int:pk>/delete/', TourDeleteView.as_view(template_name='users/tour_confirm_delete.html'), name='tour-delete'),
    path('tours/<int:pk>/', TourDetailView.as_view(template_name='users/tour_detail.html'), name='tour-detail'),
    path('pie-chart/', views.pie_chart, name='pie-chart'),
    path('population-chart/', views.home, name='population-chart'), 
]