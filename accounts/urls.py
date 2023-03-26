from django.urls import path
from .views import SignUpView, AccountProfileView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("profile/", AccountProfileView.as_view(), name="account_profile")
]