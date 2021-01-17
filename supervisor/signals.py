from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Car

@receiver(post_save, sender=User)
def create_car(sender, instance, created, **kwargs): #this is receiver
    if created:
        Car.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_car(sender, instance, **kwargs): #this is receiver
    instance.profile.save()