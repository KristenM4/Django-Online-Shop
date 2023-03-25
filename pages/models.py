from django.db import models
from accounts.models import Customer, CustomerAddress

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    image = models.ImageField(upload_to="images")
    description = models.TextField()
    stock_quantity = models.IntegerField()
    discount = models.DecimalField(decimal_places=2, max_digits=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.CharField(max_length=255, default="", unique=True, db_index=True)

    def __str__(self):
        return f"{self.name} - {self.price} - {self.category}"


class Order(models.Model):
    date = models.DateField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.ForeignKey(CustomerAddress, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f"{self.date} {self.customer}"

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
