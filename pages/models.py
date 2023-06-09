from django.db import models
from django.db.models import Value
from django.urls import reverse
from accounts.models import Customer, CustomerAddress


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

    def get_absolute_url(self):
        return reverse("detail", args=[str(self.slug)])

    def link(self):
        return reverse("detail", args=[str(self.slug)])

    def weight_in_oz(self):
        weights = {
            "Surfboards": 112,
            "Snorkels": 16,
            "Fins": 48,
            "Masks": 32
        }
        if str(self.category) in weights.keys():
            return weights[str(self.category)]
        else:
            return 48


class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField()
    RATING_CHOICES = [
    ("1", "1 - Junkyard dog"),
    ("2", "2 - Sketchy"),
    ("3", "3 - Average"),
    ("4", "4 - Sick"),
    ("5", "5 - Radical, dude!"),
    ]
    rating = models.CharField(
        max_length=2,
        choices=RATING_CHOICES,
    )


class Order(models.Model):
    date = models.DateField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.ForeignKey(CustomerAddress, on_delete=models.PROTECT, null=True)
    delivery_cost = models.DecimalField(decimal_places=2, max_digits=10, default=0, null=True)
    delivery_carrier = models.CharField(max_length=100, null=True)
    delivery_days_estimate = models.IntegerField(null=True)

    def __str__(self):
        return f"Order Number: {self.id}\nDate: {self.date}\nName: {self.customer.first_name} {self.customer.last_name}\nEmail: {self.customer.email}\nAddress: {self.address}\n"

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} - Quantity: {self.quantity} - ${self.product.price * self.quantity}"
