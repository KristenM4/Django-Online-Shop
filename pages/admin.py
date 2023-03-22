from django.contrib import admin
from .models import Product, Category, Order

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name","price", "image", "stock_quantity", 
                    "category", "description", "discount", "slug",)
    list_filter = ("category", "discount", "stock_quantity",)
    prepopulated_fields = {"slug": ("name",)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)

class OrderAdmin(admin.ModelAdmin):
    list_display = ("date", "customer", "product", "quantity",)
    list_filter = ("date", "customer", "product",)

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)