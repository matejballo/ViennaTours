from django.shortcuts import redirect, render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from supervisor.models import Car, Tour
from supervisor.forms import UserRegisterForm
from .forms import TourForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

# Create your views here.
def dashboard(request):
    #tours = {
    #    'tours' : Tour.objects.order_by("-date")[:3] #Get last 3 tours
    #}
    print(request.user)
    return render(request, 'users/index.html')#, tours)

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
