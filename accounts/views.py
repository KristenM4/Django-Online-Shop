from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy

from .forms import CustomerCreationForm
from .models import CustomerAddress
# Create your views here.


class SignUpView(CreateView):
    form_class = CustomerCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class AccountProfileView(TemplateView):
    template_name = "account_profile.html"


def delete_address(request, id):
    address = CustomerAddress.objects.get(id=id)
    address.delete()
    return redirect("account_profile")

