from django.shortcuts import redirect, render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from supervisor.models import Car, Tour
from supervisor.forms import UserRegisterForm
from .forms import TourForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Sum
from django.http import JsonResponse
from django.template import defaultfilters

import datetime
import json

# Create your views here.
def dashboard(request):

    tours = Tour.objects.filter(driverID=request.user)
    stats = {
        'today': tours.filter(date__date=datetime.date.today()).aggregate(Sum('price')).get('price__sum'),
        'total': tours.aggregate(Sum('price')).get('price__sum'),
        'silver': tours.filter(tourType="Silver").count(),
        'gold': tours.filter(tourType="Gold").count(),
        'platinum': tours.filter(tourType="Platinum").count()
    }

    labels = ['Silver', 'Gold', 'Platinum']
    data = [stats.get('silver'), stats.get('gold'), stats.get('platinum')]

    tour_info = []
    tour_prices = []

    for tour in tours:
        pom = defaultfilters.date(tour.date, "DATE_FORMAT") + " - " + tour.tourType + " tour"
        tour_info.append(pom)
        tour_prices.append(tour.price)

    json_data = json.dumps(data)
    json_labels = json.dumps(labels)
    json_prices = json.dumps(tour_prices)
    json_dates = json.dumps(tour_info)
    json_stats = json.dumps(stats)

    tours = Tour.objects.filter(driverID=request.user).order_by('-date')[:3]
    return render(request, 'users/index.html', {
        'stats': json_stats, 
        'tours': tours,
        'tourlabels': json_labels,
        'tourdata': json_data,
        'tourdates': json_dates,
        'tourprices': json_prices,
        })

def settings(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            #username = form.cleaned_data.get('username')
            #messages.success(request, f'Account created for {username}!')
            return redirect('user-settings')
    else:
        form = UserRegisterForm()
    return render(request, 'users/settings.html', {'form': form})

def listtours(request):
    if request.method == 'POST':
        #print("POST: " + request.POST.get("tour_id"))
        print(request.POST)
        return HttpResponseRedirect('display')
    tours = {
        'tours' : Tour.objects.filter(driverID=request.user)
    }

    return render(request, 'users/listtours.html', tours)

#def displaytour(request):
    #value =  request.GET.get("tour_id")
    #print("" + value)
#    print(request.POST.get)
#    tour = Tour.objects.get(id=1)
#    return render(request, 'users/tour.html', {'post': tour})


class TourListsView(ListView):
    model = Tour
    template_name = 'users/listtours.html'
    context_object_name = 'tours'
    ordering = ['-date']

    def get_queryset(self):
        return Tour.objects.filter(driverID=self.request.user)

class TourDetailView(DetailView):
    model = Tour

class TourDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tour
    success_url = "/users"

    def test_func(self):
        tour = self.get_object()
        if self.request.user == tour.driverID:
            return True
        return False    

class TourCreateView(LoginRequiredMixin, CreateView):
    model = Tour
    fields = ['carID', 'duration', 'tourType', 'people', 'price']

    def form_valid(self, form):
        tour = form.instance
        tour.driverID = self.request.user
        form.save(commit=False)
        return super().form_valid(form)

class TourUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tour
    fields = ['carID', 'duration', 'tourType', 'people', 'price']

    def form_valid(self, form):
        tour = form.instance
        tour.driverID = self.request.user
        form.save(commit=False)
        return super().form_valid(form)

    def test_func(self):
        tour = self.get_object()
        if self.request.user == tour.driverID:
            return True
        return False    

#@login_required
def profile(request):
    #user = request.user
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('user-profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

def edittour(request):
    print(request.user)
    tour = Tour.objects(tourID=request.user)
    if request.method == 'POST':
        form = TourForm(request.POST, instance=tour)
        if form.is_valid():

            form.save()
            #username = form.cleaned_data.get('username') #TODO change
            #messages.success(request, f'Account created for {username}!')
            return redirect('user-tours')
   
    return render(request, 'users/addtour.html', {'form': form})


def addtour(request):
    if request.method == 'POST':
        form = TourForm(request.POST)
        if form.is_valid():
            tour = form.instance
            tour.driverID = request.user
            form.save()
            #username = form.cleaned_data.get('username') #TODO change
            #messages.success(request, f'Account created for {username}!')
            return redirect('user-tours')
    else:
        form = TourForm()
    print(request.user)
    return render(request, 'users/addtour.html', {'form': form})

def pie_chart(request):
    tours = Tour.objects.filter(driverID=request.user)
    stats = {
        'silver': tours.filter(tourType="Silver").count(),
        'gold': tours.filter(tourType="Gold").count(),
        'platinum': tours.filter(tourType="Platinum").count()
    }    
    labels = ['Silver', 'Gold', 'Platinum']
    data = [stats.get('silver'), stats.get('gold'), stats.get('platinum')]

    json_string = json.dumps(stats)
    json_data = json.dumps(data)
    json_labels = json.dumps(labels)

    return render(request, 'users/pie_chart.html', {
        'tourlabels': json_labels,
        'tourdata': json_data,
        'stats': json_string,
    })

def home(request):
    return render(request, 'users/home.html')

def getTours(request):
    tours_list = Tour.objects.all().values("tourType", "price")
    return JsonResponse(tours_list)