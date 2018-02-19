from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.deletion import CASCADE

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    country = models.CharField(max_length=32, verbose_name="Country of origin", name="country", blank=True, null=True)
    phone = models.CharField(max_length=32, verbose_name="Phone", name="phone", blank=True, null=True)
    occupation_field = models.CharField(max_length=32, verbose_name="Occupation Field", name="occupation_field", blank=True, null=True)
    occupation = models.CharField(max_length=32, verbose_name="Occupation", name="occupation", blank=True, null=True)
    birthdate = models.DateField(verbose_name="Birth Date", name="birthdate", auto_now_add=False, auto_now=False, blank=True, null=True)
    description = models.TextField(verbose_name="Description", name="description", blank=True, null=True)
    
    def __str__(self):
        return self.user.first_name

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Person.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.person.save()