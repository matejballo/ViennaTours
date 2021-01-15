from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from supervisor.models import Tour, Car

class CarForm(ModelForm):
    class Meta:
        model = Car
        fields = ['latitude', 'longitude', 'photoOption']

class TourForm(ModelForm):
    class Meta:
        model = Tour
        fields = ['carID', 'duration', 'tourType', 'people', 'price']
    