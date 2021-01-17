from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from urllib.request import urlopen
from django.utils.safestring import SafeString
from .models import Tour, Car
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegisterForm, CarRegistrationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import (CreateView)
import json
from django.http import JsonResponse

# Create your views here.
def dashboard(request):
    tours = {
        'tours' : Tour.objects.order_by("-date")[:3] #Get last 3 tours
    }
    return render(request, 'supervisor/index.html', tours)

def employees(request):
    return render(request, 'supervisor/employees.html')

def settings(request):
    users = {
        'employees' : User.objects.all()
    }
    return render(request, 'supervisor/settings.html', users)

def vehicles(request):
    return render(request, 'supervisor/vehicles.html')

def listdata(request):
    tours = {
        'tours' : Tour.objects.all()
    }
    return render(request, 'supervisor/list.html', tours)

def listcar(request):
    cars = {
        'cars' : Car.objects.all()
    }
    return render(request, 'supervisor/listcar.html', cars)

def registration(request): #TODO add more info
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('supervisor-settings')
    else:
        form = UserRegisterForm()
    return render(request, 'supervisor/editor.html', {'form': form})


def createcar(request): #TODO add more info
    if request.method == 'POST':
        form = CarRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            #username = form.cleaned_data.get('car')
            #messages.success(request, f'Account created for {username}!')
            return redirect('supervisor-listcar')
    else:
        form = CarRegistrationForm()
    return render(request, 'supervisor/addcar.html', {'form': form})

def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)