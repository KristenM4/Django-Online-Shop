from django.urls import path
from . import views

urlpatterns = [
    path("product/<slug:slug>", views.DetailPageView.as_view(), name="detail"),
    path("", views.HomePageView.as_view(), name="home"),
]