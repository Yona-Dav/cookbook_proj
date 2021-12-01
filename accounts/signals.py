from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, User


@receiver(post_save, sender=User)
def my_callback(sender, instance, created, **kwargs):
    if created:  #if user created
        Profile.objects.create(user=instance) #you can create a profile for the user