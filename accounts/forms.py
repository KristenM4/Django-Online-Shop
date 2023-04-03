from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Customer

BIRTH_YEAR_CHOICES = [x for x in range(1930,2023)]

class CustomerCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    date_of_birth = forms.DateField(
        required=True,
        initial="1990-01-01",
        widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES)
    )

    class Meta(UserCreationForm):
        model = Customer
        fields = UserCreationForm.Meta.fields + ("email", "first_name", "last_name", "date_of_birth",)

class CustomerChangeForm(UserChangeForm):
    class Meta:
        model = Customer
        fields = UserChangeForm.Meta.fields