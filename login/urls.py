from . import views
from django.contrib.auth import views as auth_views
from django.urls import path, re_path

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    re_path(r'^login_success/$', views.login_success, name='login_success'),
]
