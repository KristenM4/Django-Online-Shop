from django.db import models
from accounts.models import Customer

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    image = models.ImageField(upload_to="images")
    description = models.TextField()
    stock_quantity = models.IntegerField()
    discount = models.DecimalField(decimal_places=2, max_digits=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Order(models.Model):
    date = models.DateField(auto_now_add=True)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product,)
