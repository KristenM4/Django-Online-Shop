from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic import CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from .models import Product, Order, OrderItem
from accounts.models import CustomerAddress
from cart.cart import Cart

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
        cat_items = Product.objects.filter(category__name=category.title())
        return render(request, "cat.html", {"category": cat_items})
    

@login_required(login_url="/accounts/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def cart_detail(request):
    total_amt = 0
    try:
        for id,item in request.session['cart'].items():
            total_amt+= int(item['quantity'])*float(item['price'])
    except KeyError:
        return redirect("home")
    else:
        return render(request, 'cart_detail.html', {'total': total_amt})


class AddressFormView(LoginRequiredMixin, CreateView):
    template_name = "address.html"
    model = CustomerAddress
    fields = ("address_one", "address_two", "city", "state", "zipcode", "country",)

    def form_valid(self, form):
        form.instance.customer = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('place_order',args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["addresses"] = self.request.user.customeraddress_set.all()
        total_amt = 0
        for id,item in self.request.session['cart'].items():
            total_amt+= int(item['quantity'])*float(item['price'])
        context["total"] = total_amt
        return context

class PlaceOrderView(DetailView):
    model = CustomerAddress
    template_name = "place_order.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        total_amt = 0
        for id,item in self.request.session['cart'].items():
            total_amt+= int(item['quantity'])*float(item['price'])
        context["total"] = total_amt
        return context