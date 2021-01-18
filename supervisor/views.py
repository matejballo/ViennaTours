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
from django.http import JsonResponse
from django.db.models import Count
from django.db.models import Sum
from django.template import defaultfilters
import json
import datetime


################
#
#
#   TOURS
#
#List all tours
class ToursListsView(ListView):
    model = Tour
    template_name = 'supervisor/tours_list.html'
    context_object_name = 'tours'

    def get_queryset(self):
        return Tour.objects.all()

#Delete specific Tour
class TourDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tour
    success_url = "/supervisor/tours"

    def test_func(self):
        return True    

#Show tour details
class TourDetailsView(DetailView):
    model = Tour

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
def vehicle_add(request):
    if request.method == 'POST':
        form = CarRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'New vehicle has been created!')
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
        return True 

################
#
#
#   OTHER
#
#Dashboard
def dashboard(request):
    tours = Tour.objects.all()
    bestdriver_id = Tour.objects.values("driverID").annotate(c=Count('driverID')).order_by('-c').first()['driverID']
    bestdriver = User.objects.get(id=bestdriver_id)
        
    stats = {
        'today': tours.filter(date__date=datetime.date.today()).aggregate(Sum('price')).get('price__sum'),
        'total': tours.aggregate(Sum('price')).get('price__sum'),
        'silver': tours.filter(tourType="Silver").count(),
        'gold': tours.filter(tourType="Gold").count(),
        'platinum': tours.filter(tourType="Platinum").count(),
        'silver_total': tours.filter(tourType="Silver").aggregate(Sum('price')),
        'gold_total': tours.filter(tourType="Gold").aggregate(Sum('price')),
        'platinum_total': tours.filter(tourType="Platinum").aggregate(Sum('price')),


    }
    labels = ['Silver', 'Gold', 'Platinum']
    data = [stats.get('silver'), stats.get('gold'), stats.get('platinum')]
    data_prices = [stats.get('silver_total')['price__sum'], stats.get('gold_total')['price__sum'], stats.get('platinum_total')['price__sum']]

    tour_info = []
    tour_prices = []
    tour_people = []

    for tour in tours:
        pom = defaultfilters.date(tour.date, "DATE_FORMAT") + " - " + tour.tourType + " tour"
        tour_info.append(pom)
        tour_prices.append(tour.price)
        tour_people.append(tour.people)

    json_data = json.dumps(data)
    json_data_prices = json.dumps(data_prices)
    json_labels = json.dumps(labels)
    json_prices = json.dumps(tour_prices)
    json_people = json.dumps(tour_people)
    json_dates = json.dumps(tour_info)
    json_stats = json.dumps(stats)

    print(json_data_prices)

    tours = tours.order_by('-date')[:3]
    return render(request, 'supervisor/index.html', {
        'stats': json_stats, 
        'best_driver': bestdriver,
        'last_tours': tours,
        'tourlabels': json_labels,
        'tourdata': json_data_prices,
        'tourdates': json_dates,
        'tourprices': json_people,
        })

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