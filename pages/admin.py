from django.contrib import admin
from .models import Product, Category, Order, OrderItem, Review

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name","price", "image", "stock_quantity", 
                    "category", "description", "discount", "slug",)
    list_filter = ("category", "discount", "stock_quantity",)
    prepopulated_fields = {"slug": ("name",)}

class ProductInline(admin.TabularInline):
    model = Product
    extra = 0

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [ProductInline,]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ("date", "customer",)
    list_filter = ("date", "customer",)
    inlines = [OrderItemInline,]

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity", "order")
    list_filter = ("order",)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "customer", "rating", "text",)
    list_filter = ("product", "customer", "rating",)

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Review, ReviewAdmin)