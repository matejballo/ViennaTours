from django.shortcuts import render
from supervisor.models import Tour, Car
from supervisor.forms import UserRegisterForm
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def dashboard(request):
    #tours = {
    #    'tours' : Tour.objects.order_by("-date")[:3] #Get last 3 tours
    #}
    return render(request, 'users/index.html')#, tours)

def settings(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('supervisor-settings')
    else:
        form = UserRegisterForm()
    return render(request, 'users/settings.html', {'form': form})

def listtours(request):
    tours = {
        'tours' : Tour.objects.all()
    }
    return render(request, 'users/listtours.html', tours)

def addtour(request):
    return render(request, 'users/addtour.html')