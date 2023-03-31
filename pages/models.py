from django.db import models
from django.db.models import Value
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
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    image = models.ImageField(upload_to="images")
    description = models.TextField()
    stock_quantity = models.IntegerField()
    discount = models.DecimalField(decimal_places=2, max_digits=2, default=.00)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.CharField(max_length=255, default="", unique=True, db_index=True)

    def __str__(self):
        return f"{self.name} - {self.price} - {self.category}"
    
    def discount_price(self):
        return round(self.price - (self.price * self.discount), 2)


class Order(models.Model):
    date = models.DateField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.ForeignKey(CustomerAddress, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f"Order Number: {self.id}\nDate: {self.date}\nName: {self.customer.first_name} {self.customer.last_name}\nEmail: {self.customer.email}\nAddress: {self.address}\n"

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} - Quantity: {self.quantity} - ${self.product.price * self.quantity}"
