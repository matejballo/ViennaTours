from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
def login_success(request):
    if request.user.is_superuser:
        #your logic here
        return redirect('supervisor-dashboard')
    else:
        #your logic here
        return redirect('user-dashboard')