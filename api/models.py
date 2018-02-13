from django.db import models
from django.core.validators import RegexValidator, validate_email

class Person(models.Model):
    firstname = models.CharField(max_length=32, verbose_name="First Name", name="firstname", blank=False, null=False,
                                 validators=[RegexValidator(regex='^[A-z-]{1,32}$', message='First name must only contain letters (without accents), spaces and hyphens')])
    lastname = models.CharField(max_length=32, verbose_name="Last Name", name="lastname", blank=True, null=True)
    country = models.CharField(max_length=32, verbose_name="Country of origin", name="country", blank=True, null=True)
    email = models.CharField(max_length=64, verbose_name="Email", name="email", blank=True, null=True,
                             validators=[validate_email])
    phone = models.CharField(max_length=32, verbose_name="Phone", name="phone", blank=True, null=True)
    occupation_field = models.CharField(max_length=32, verbose_name="Occupation Field", name="occupation_field", blank=True, null=True)
    occupation = models.CharField(max_length=32, verbose_name="Occupation", name="occupation", blank=True, null=True)
    birthdate = models.DateField(verbose_name="Birth Date", name="birthdate", auto_now_add=False, auto_now=False, blank=True, null=True)
    description = models.TextField(verbose_name="Description", name="description", blank=True, null=True)
    
    def __str__(self):
        return self.firstname