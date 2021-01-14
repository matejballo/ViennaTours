from django.shortcuts import render
#from .models import Tour

# Create your views here.
def dashboard(request):
    #tours = {
    #    'tours' : Tour.objects.order_by("-date")[:3] #Get last 3 tours
    #}
    return render(request, 'users/index.html')#, tours)

def settings(request):
    #tours = {
    #    'tours' : Tour.objects.order_by("-date")[:3] #Get last 3 tours
    #}
    return render(request, 'users/settings.html')#, tours)