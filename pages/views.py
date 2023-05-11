from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.views import View
from django.views.generic import CreateView, FormView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.urls import reverse

from cart.cart import Cart
from decouple import config
import requests
import json
import smtplib
from .forms import ReviewForm
from .models import Product, Order, OrderItem
from accounts.models import CustomerAddress


class HomePageView(ListView):
    template_name = "home.html"
    model = Product
    context_object_name = "products"
    queryset = Product.objects.all().order_by("slug")[:8]


class AboutPageView(TemplateView):
    template_name = "about.html"


class ApiInfoView(TemplateView):
    template_name = "api_info.html"


class CategoryPageView(TemplateView):
    template_name = "cat.html"

    def get(self, request, category):
        cat_items = Product.objects.filter(category__name=category.title())
        return render(request, "cat.html", {"category": cat_items})


# Views for handling product detail page, including product reviews


class DetailPageView(DetailView):
    model = Product
    template_name = "detail.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        current_product = self.get_object()
        context["related"] = Product.objects.filter(category__name=current_product.category.name)[:4]
        context["form"] = ReviewForm
        context["review_list"] = current_product.review_set.all().order_by("-id")
        # review pagination
        review_list = current_product.review_set.all().order_by("-id")
        paginator = Paginator(review_list, 5)
        customer = self.request.user
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["page_obj"] = page_obj
        # for loop checks if user has bought/reviewed the item
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
        if self.object.review_set.filter(customer=self.request.user):
            user_review = self.object.review_set.filter(customer=self.request.user)[0]
            user_review.rating = review.rating
            user_review.text = review.text
            user_review.save()
        else:
            review.customer = self.request.user
            review.product = self.object
            review.save()
        return super().form_valid(form)

    def get_success_url(self):
        product = self.get_object()
        return reverse("detail", kwargs={'slug': product.slug})


class DetailPageUpdateView(DetailView):
    model = Product
    template_name = "detail.html"
    form_class = ReviewForm

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        current_product = self.get_object()
        user_review = current_product.review_set.filter(customer=self.request.user)[0]
        context["related"] = Product.objects.filter(category__name=current_product.category.name)[:4]
        context["form"] = ReviewForm
        context["review_list"] = current_product.review_set.all().order_by("-id")
        # review pagination
        review_list = current_product.review_set.all().order_by("-id")
        paginator = Paginator(review_list, 5)
        customer = self.request.user
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["page_obj"] = page_obj

        context["update_form"] = ReviewForm(instance=user_review)
        context["has_bought"] = True
        context["has_reviewed"] = True
        context["update_review"] = True

        return context


class DetailPageDeleteView(DetailView):
    model = Product
    template_name = "detail.html"
    form_class = ReviewForm

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        current_product = self.get_object()
        customer = self.request.user
        user_review = current_product.review_set.filter(customer=self.request.user)[0]
        if user_review.customer == self.request.user:
            user_review.delete()
        context["related"] = Product.objects.filter(category__name=current_product.category.name)[:4]
        context["form"] = ReviewForm
        context["delete_review"] = True
        context["review_list"] = current_product.review_set.all().order_by("-id")
        # review pagination
        review_list = current_product.review_set.all().order_by("-id")
        paginator = Paginator(review_list, 5)
        customer = self.request.user
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["page_obj"] = page_obj
        # for loop checks if user has bought/reviewed the item
        context["has_bought"] = True
        context["has_reviewed"] = False
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


class ProductDetailView(View):

    def get(self, request, *args, **kwargs):
        if "update_review_button" in self.request.GET:
            view = DetailPageUpdateView.as_view()
            return view(request, *args, **kwargs)
        elif "delete_review_button" in self.request.GET:
            view = DetailPageDeleteView.as_view()
            return view(request, *args, **kwargs)
        else:
            view = DetailPageView.as_view()
            return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if "create_review_button" in self.request.POST:
            view = DetailPagePostView.as_view()
            return view(request, *args, **kwargs)
        elif "update_review_button" in self.request.POST:
            view = DetailPagePostView.as_view()
            return view(request, *args, **kwargs)
        elif "delete_review_button" in self.request.POST:
            view = DetailPageDeleteView.as_view()
            return view(request, *args, **kwargs)


# Cart functions

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

# Views for order placement and checkout


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
    # Gets shipping estimate, creates order object, sends customer email with order details
    model = CustomerAddress
    template_name = "place_order.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        object = self.get_object()
        total_amt = 0
        total_weight = 0
        for id,item in self.request.session['cart'].items():
            product = Product.objects.get(name=item["name"])
            total_weight += int(product.weight_in_oz())
            total_amt+= int(item['quantity'])*float(item['price'])
        context["total"] = total_amt
        api_key = config("SHIPENGINE_API_KEY")
        endpoint = "https://api.shipengine.com/v1/rates"
        payload = json.dumps({
            "rate_options": {
                "carrier_ids": [
                "se-4697523"
                ]
            },
            "shipment": {
                "validate_address": "no_validation",
                "ship_to": {
                    "name": f"{self.request.user.first_name} {self.request.user.last_name}",
                    "phone": "222-333-4444",
                    "company_name": "",
                    "address_line1": f"{object.address_one} {object.address_two}",
                    "city_locality": object.city,
                    "state_province": object.state,
                    "postal_code": object.zipcode,
                    "country_code": str(object.country),
                    "address_residential_indicator": "no"
                },
                "ship_from": {
                    "name": "Sea Wolf Surf and Dive Shop",
                    "phone": "222-333-4444",
                    "company_name": "The Sea Wolf",
                    "address_line1": "84-521 Farrington Highway",
                    "city_locality": "Waianae",
                    "state_province": "HI",
                    "postal_code": "96792",
                    "country_code": "US",
                    "address_residential_indicator": "no"
                },
                "packages": [
                {
                    "package_code": "package",
                    "weight": {
                        "value": total_weight,
                        "unit": "ounce"
                    }
                }
                ]
            },
        })
        headers = {
            "Host": "api.shipengine.com",
            "API-Key": api_key,
            "Content-Type": "application/json"
        }
        try:
            response = requests.request("POST", url=endpoint, headers=headers, data=payload)
            response = response.json()
            print(response)
            try:
                context["delivery_total"] = response["rate_response"]["rates"][0]["shipping_amount"]["amount"]
                context["delivery_currency"] = response["rate_response"]["rates"][0]["shipping_amount"]["currency"].upper()
                context["delivery_days"] = response["rate_response"]["rates"][0]["delivery_days"]
                context["service_type"] = response["rate_response"]["rates"][0]["service_type"]
            except IndexError:
                context["delivery_total"] = response["rate_response"]["invalid_rates"][0]["shipping_amount"]["amount"]
                context["delivery_currency"] = response["rate_response"]["invalid_rates"][0]["shipping_amount"]["currency"].upper()
                context["delivery_days"] = response["rate_response"]["invalid_rates"][0]["delivery_days"]
                context["service_type"] = response["rate_response"]["invalid_rates"][0]["service_type"]
        except TypeError:
            context["delivery_total"] = 25
            context["delivery_currency"] = "USD"
            context["delivery_days"] = 5
            context["service_type"] = "USPS"
        context["order_total"] = total_amt + context["delivery_total"]
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        delivery_currency = context["delivery_currency"]
        delivery_days = context["delivery_days"]
        carrier = context["service_type"]
        delivery_total = round(context["delivery_total"], 2)
        company_email = config("EMAIL_HOST_USER")
        company_pass = config("EMAIL_HOST_PASSWORD")
        address = CustomerAddress.objects.get(pk=self.kwargs["pk"])
        customer = self.request.user

        new_order = Order.objects.create(
            customer=customer,
            address=address,
            delivery_cost=delivery_total,
            delivery_carrier=carrier,
            delivery_days_estimate=delivery_days,
        )
        for id,item in self.request.session["cart"].items():
            product = Product.objects.get(name=item["name"])
            new_item = OrderItem.objects.create(product=product, quantity=item["quantity"], order=new_order)

        items_message = ""
        for item in new_order.orderitem_set.all():
            items_message += f"{item}\n"
        if delivery_days != None:
            delivery_message = f"Delivery cost: {delivery_total} {delivery_currency}\nEstimated delivery time: {delivery_days} business days\nCarrier: {carrier}"
        else:
            delivery_message = f"Delivery cost: {delivery_total} {delivery_currency}\nEstimated delivery time is unavailable.\nCarrier: {carrier}"
        full_total = round(context["order_total"], 2)

        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            message = f"Thanks for the order, {customer.first_name}! Order details are below:\n\n{new_order}\n{items_message}\n{delivery_message}\n\nOrder Total: ${full_total}"
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
