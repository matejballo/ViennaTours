from django.contrib import admin
from .models import Car, Tour, Supervisor

# Register your models here.
admin.site.register(Car)
admin.site.register(Tour)
admin.site.register(Supervisor)