from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from PIL import Image


class Supervisor(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)

# Create your models here.
class Car(models.Model):
    plate = models.CharField(max_length=4, unique=True)
    photoOption = models.ImageField(default='car-black.jpg', upload_to='cars_pics/')

    def __str__(self):
        return str(self.plate)

    def save(self):
        super().save()

        img = Image.open(self.photoOption.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photoOption.path)


class Tour(models.Model):
    TOUR_CHOICES = (('Silver', 'Silver'), ('Gold', 'Gold'), ('Platinum', 'Platinum'))

    driverID = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)  #TODO change to something else. If User is deleted, delete tours?
    carID = models.ForeignKey(Car, null=True, on_delete=models.SET_NULL) #TODO change to something else
       
    date = models.DateTimeField(default=timezone.now) 
    duration = models.FloatField()
    tourType = models.CharField(max_length=20, choices=TOUR_CHOICES, default='Silver')
    people = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return self.tourType

    def get_absolute_url(self):
        return reverse('tour-detail', kwargs={'pk': self.pk})
        
