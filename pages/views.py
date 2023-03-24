from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Product

# Create your views here.


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_products = Product.objects.all()
        context["products"] = all_products
        return context

class DetailPageView(DetailView):
    model = Product
    template_name = "detail.html"

class CategoryPageView(TemplateView):
    template_name = "cat.html"

    def get(self, request, category):
        first_item = Product.objects.all()[0]
        print(first_item.category.name)
        cat_items = Product.objects.filter(category__name=category.title())
        print(cat_items)
        return render(request, "cat.html", {"category": cat_items})

