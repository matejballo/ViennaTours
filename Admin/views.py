from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def dashboard(request):
    return render(request, 'admin/index.html')

def employees(request):
    return render(request, 'admin/employees.html')

def settings(request):
    return render(request, 'admin/settings.html')

def vehicles(request):
    return render(request, 'admin/vehicles.html')