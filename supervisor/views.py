from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from urllib.request import urlopen
from django.utils.safestring import SafeString
from .models import Tour
from .models import Car
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CarRegistrationForm, SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (CreateView, ListView, DeleteView, DetailView)
import json
from django.http import JsonResponse

################
#
#
#   TOURS
#
#List all tours
def tours_list(request):
    tours = {
        'tours' : Tour.objects.all()
    }
    return render(request, 'supervisor/tours_list.html', tours)

class ToursListsView(ListView):
    model = Tour
    template_name = 'supervisor/tours_list.html'
    context_object_name = 'tours'

    def get_queryset(self):
        return Tour.objects.all()



################
#
#
#   EMPLOYEES
#
#List employees
class EmployeesListsView(ListView):
    model = User
    template_name = 'supervisor/employees_list.html'
    context_object_name = 'employees'

    def get_queryset(self):
        return User.objects.all().filter(is_staff=False)

#Generic class to show details for specific Tour
class EmployeeDetailsView(DetailView):
    model = User

class EmployeeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    success_url = "/supervisor/employees"

    def test_func(self):
        model = self.get_object()
        if self.request.user == self.request.user: #TODO zmen
            return True
        return False    


#Create new employee
def employee_add(request): #TODO add more info
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            print("SIGNUP FORM IS VALID")
            form.save()
            #TODO messages.success(request, f'Account created for {username}!')
            return redirect('supervisor-employees-list')
        else:
            print("ERROR : ", form.errors)
    else:
        form = SignUpForm()
    return render(request, 'supervisor/employee_form.html', {'form': form})


################
#
#
#   VEHICLES
#
#Create new vehicle
def vehicle_add(request): #TODO add more info
    if request.method == 'POST':
        form = CarRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            #TODO messages.success(request, f'Account created for {username}!')
            return redirect('supervisor-vehicles-list')
    else:
        form = CarRegistrationForm()
    return render(request, 'supervisor/vehicle_add.html', {'form': form})

#List all available vehicles
class VehicleListsView(ListView):
    model = Car
    template_name = 'supervisor/vehicles_list.html'
    context_object_name = 'cars'

    def get_queryset(self):
        return Car.objects.all()

#Delete specific vehicle
class VehicleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Car
    success_url = "/supervisor/vehicles"

    def test_func(self):
        car = self.get_object()
        if self.request.user == self.request.user: #TODO zmen
            return True
        return False    

################
#
#
#   OTHER
#
#Dashboard
def dashboard(request):
    tours = {
        'tours' : Tour.objects.order_by("-date")[:3] #Get last 3 tours
    }
    return render(request, 'supervisor/index.html', tours)

#Admin settings
def settings(request):
    users = {
        'employees' : User.objects.all()
    }
    return render(request, 'supervisor/admin_settings.html', users)

################
#
#
#   AJAX
#
#Check if username already exists
def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

#Check if plate of car already exists
def validate_plate(request):
    plate = request.GET.get('plate', None)
    data = {
        'is_taken': Car.objects.filter(plate=plate).exists()
    }
    return JsonResponse(data)