from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Customer

class CustomerCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Customer
        fields = UserCreationForm.Meta.fields + ("date_of_birth",)

class CustomerChangeForm(UserChangeForm):
    class Meta:
        model = Customer
        fields = UserChangeForm.Meta.fields