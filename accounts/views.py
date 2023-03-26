from django.shortcuts import redirect
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.db.models import ProtectedError

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
    try:
        address.delete()
    except ProtectedError:
        address.hidden = True
        address.save()
    return redirect("account_profile")

class NewAddressView(CreateView):
    model = CustomerAddress
    template_name = "new_address.html"
    success_url = reverse_lazy("account_profile")
    fields = ("address_one", "address_two", "city", "state", "zipcode", "country",)

    def form_valid(self, form):
        form.instance.customer = self.request.user
        return super().form_valid(form)

