from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField

# Create your models here.

class CustomerAddress(models.Model):
    address_one = models.CharField(max_length=300)
    address_two = models.CharField(max_length=300, blank=True)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=2, blank=True)
    zipcode = models.IntegerField()
    country = CountryField()

class Customer(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)