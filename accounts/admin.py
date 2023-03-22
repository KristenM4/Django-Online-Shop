from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomerCreationForm, CustomerChangeForm
from .models import Customer

# Register your models here.

class CustomerAdmin(UserAdmin):
    add_form = CustomerCreationForm
    form = CustomerChangeForm
    model = Customer
    list_display = ["email", "username", "date_of_birth", "postal_address", "is_staff",]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("date_of_birth", "postal_address",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("date_of_birth", "postal_address",)}),)

admin.site.register(Customer, CustomerAdmin)