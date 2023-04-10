from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.views import View
from django.views.generic import CreateView, FormView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from cart.cart import Cart
from decouple import config
import smtplib
from .models import Product, Order, OrderItem, Review
from accounts.models import CustomerAddress

# Create your views here.


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_products = Product.objects.all().order_by("slug")[:8]
        context["products"] = all_products
        return context

class AboutPageView(TemplateView):
    template_name = "about.html"

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("rating", "text",)

class DetailPageView(DetailView):
    model = Product
    template_name = "detail.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        current_product = self.get_object()
        context["related"] = Product.objects.filter(category__name=current_product.category.name)[:4]
        context["form"] = ReviewForm
        customer = self.request.user
        context["has_bought"] = False
        context["has_reviewed"] = False
        has_bought = False
        has_reviewed = False
        if customer.username != "":
            for item in customer.order_set.all():
                for product in item.orderitem_set.all():
                    if product.product == current_product:
                        context["has_bought"] = True
                        has_bought = True
                        context["bought_date"] = item.date
            if has_bought:
                for review in customer.review_set.all():
                    if current_product == review.product:
                        context["has_reviewed"] = True
                        has_reviewed = True
                        break

        return context

class DetailPagePostView(SingleObjectMixin, FormView):
    model = Product
    template_name = "detail.html"
    form_class = ReviewForm

    def post(self, request, *args, **kwargs):
        customer = self.request.user
        if customer.username == "":
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form):
        review = form.save(commit=False)
        review.customer = self.request.user
        review.product = self.object
        review.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        product = self.get_object()
        return reverse("detail", kwargs={'slug': product.slug})


class ProductDetailView(View):

    def get(self, request, *args, **kwargs):
        view = DetailPageView.as_view()
        return view(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if "create_review_button" in self.request.POST:
            view = DetailPagePostView.as_view()
            return view(request, *args, **kwargs)
        elif "update_review_button" in self.request.POST:
            pass
        elif "delete_review_button" in self.request.POST:
            pass


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
    
    def post(self, request, *args, **kwargs):
        company_email = config("EMAIL_HOST_USER")
        company_pass = config("EMAIL_HOST_PASSWORD")
        address = CustomerAddress.objects.get(pk=self.kwargs["pk"])
        customer = self.request.user

        new_order = Order.objects.create(customer=customer, address=address)
        for id,item in self.request.session["cart"].items():
            product = Product.objects.get(name=item["name"])
            new_item = OrderItem.objects.create(product=product, quantity=item["quantity"], order=new_order)

        items_message = ""
        items_total = 0
        for item in new_order.orderitem_set.all():
            items_message += f"{item}\n"
            items_total += round(item.product.price * item.quantity, 2)

        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            message = f"Thanks for the order, {customer.first_name}! Order details are below:\n\n{new_order}\n{items_message}\nOrder Total: ${items_total}"
            connection.starttls()
            connection.login(user=company_email, password=company_pass)
            final_message = f"Subject: Thank you for your order!\n\n{message}"
            connection.sendmail(from_addr=company_email, to_addrs=customer.email, msg=final_message)
            connection.close()

        cart = Cart(request)
        cart.clear()

        return redirect("order_success")

class OrderSuccessView(TemplateView):
    template_name = "order_success.html"