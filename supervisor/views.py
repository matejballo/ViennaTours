from django.shortcuts import render

# Create your views here.
# Create your views here.
def dashboard(request):
    return render(request, 'supervisor/index.html')

def employees(request):
    return render(request, 'supervisor/employees.html')

def settings(request):
    return render(request, 'supervisor/settings.html')

def vehicles(request):
    return render(request, 'supervisor/vehicles.html')