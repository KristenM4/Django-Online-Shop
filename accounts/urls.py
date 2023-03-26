from django.urls import path
from .views import SignUpView, AccountProfileView, delete_address, NewAddressView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("profile/", AccountProfileView.as_view(), name="account_profile"),
    path("delete_address/<int:id>/", delete_address, name="delete_address"),
    path("new_address/", NewAddressView.as_view(), name="new_address"),
]