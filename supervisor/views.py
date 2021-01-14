from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from urllib.request import urlopen
from django.utils.safestring import SafeString
from .models import Tour, Employee
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def dashboard(request):
    tours = {
        'tours' : Tour.objects.order_by("-date")[:3] #Get last 3 tours
    }
    return render(request, 'supervisor/index.html', tours)

def employees(request):
    return render(request, 'supervisor/employees.html')

def settings(request):
    employees = {
        'employees' : Employee.objects.all()
    }
    return render(request, 'supervisor/settings.html', employees)

def vehicles(request):
    return render(request, 'supervisor/vehicles.html')

def listdata(request):
    tours = {
        'tours' : Tour.objects.all()
    }
    return render(request, 'supervisor/list.html', tours)

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