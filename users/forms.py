from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from supervisor.models import Tour, Car
from users.models import Profile

class CarForm(ModelForm):
    class Meta:
        model = Car
        fields = ['latitude', 'longitude', 'photoOption']

class TourForm(forms.ModelForm):
    TOUR_OPTIONS = (('silver', 'Silver'), ('gold', 'Gold'), ('platinum', 'Platinum'))
    tourType = forms.ChoiceField(choices=TOUR_OPTIONS)

    class Meta:
        model = Tour
        fields = ['carID', 'duration', 'tourType', 'people', 'price']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.TextInput()
    last_name = forms.TextInput()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
    