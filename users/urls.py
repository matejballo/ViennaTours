from . import views
from django.urls import path

urlpatterns = [
    path('', views.dashboard, name='user-dashboard'),
    path('settings/', views.settings, name='user-settings'),
    path('tours/', views.listtours, name='user-tours'),
    path('tours/addtour/', views.addtour, name='user-tour-add'),
]
