from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.contrib.auth.models import PermissionsMixin

# Create your models here.


class Customer(AbstractUser, PermissionsMixin):
    date_of_birth = models.DateField(null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()


class CustomerAddress(models.Model):
    address_one = models.CharField(max_length=300)
    address_two = models.CharField(max_length=300, blank=True)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=2, blank=True)
    zipcode = models.IntegerField()
    country = CountryField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.address_one} {self.address_two} {self.zipcode} {self.city}, {self.state} {self.country}"