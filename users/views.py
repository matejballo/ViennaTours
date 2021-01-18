from django.shortcuts import redirect, render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from supervisor.models import Car, Tour
from supervisor.forms import SignUpForm
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


#
#
#   TOURS
#
#
#Generic class for listing user Tours
class TourListsView(ListView):
    model = Tour
    template_name = 'users/tours_list.html'
    context_object_name = 'tours'
    ordering = ['-date']

    def get_queryset(self):
        return Tour.objects.filter(driverID=self.request.user)

#Generic class to show details for specific Tour
class TourDetailView(DetailView):
    model = Tour

#Generic class for deleting specific Tour
class TourDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tour
    success_url = "/users"

    def test_func(self):
        tour = self.get_object()
        if self.request.user == tour.driverID:
            return True
        return False    

#Generic class for creating new Tours
class TourCreateView(LoginRequiredMixin, CreateView):
    model = Tour
    fields = ['carID', 'duration', 'tourType', 'people', 'price']

    def form_valid(self, form):
        tour = form.instance
        tour.driverID = self.request.user
        form.save(commit=False)
        return super().form_valid(form)

#Generic class for editing selected Tour
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

#
#
#   OTHER
#
#
#Dashboard view
def dashboard(request):
    #Get only current user tours
    tours = Tour.objects.filter(driverID=request.user)
    
    #General stats
    stats = {
        'today': tours.filter(date__date=datetime.date.today()).aggregate(Sum('price')).get('price__sum'),
        'total': tours.aggregate(Sum('price')).get('price__sum'),
    }

    #Count number of tours by its type
    labels = ['Silver', 'Gold', 'Platinum']
    data = [
        tours.filter(tourType="Silver").count(), 
        tours.filter(tourType="Gold").count(), 
        tours.filter(tourType="Platinum").count()
        ]

    #Get tours by date
    tour_info = []
    tour_prices = []
    for tour in tours:
        pom = defaultfilters.date(tour.date, "DATE_FORMAT") + " - " + tour.tourType + " tour"
        tour_info.append(pom)
        tour_prices.append(tour.price)

    #Parse to JSON for chart.js
    json_data = json.dumps(data)
    json_labels = json.dumps(labels)
    json_prices = json.dumps(tour_prices)
    json_dates = json.dumps(tour_info)
    json_stats = json.dumps(stats)

    #Get only last 3 tours
    tours = tours.order_by('-date')[:3]

    #Send data to template
    return render(request, 'users/index.html', {
        'stats': json_stats, 
        'tours': tours,
        'tourlabels': json_labels,
        'tourdata': json_data,
        'tourdates': json_dates,
        'tourprices': json_prices,
        })

#User profile
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            #Update user and profile info
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('user-profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
