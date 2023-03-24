from django.urls import path
from . import views

urlpatterns = [
    path("product/<slug:slug>", views.DetailPageView.as_view(), name="detail"),
    path("category/<category>", views.CategoryPageView.as_view(), name="category"),
    path("", views.HomePageView.as_view(), name="home"),
    
    path("cart/add/<int:id>/", views.cart_add, name="cart_add"),
    path("cart/item_clear/<int:id>/", views.item_clear, name="item_clear"),
    path("cart/item_increment/<int:id>/", views.item_increment, name="item_increment"),
    path("cart/item_decrement/<int:id>/", views.item_decrement, name="item_decrement"),
    path("cart/cart_clear/", views.cart_clear, name="cart_clear"),
    path("cart/cart-detail/",views.cart_detail,name="cart_detail"),
    path("checkout/address", views.AddressFormView.as_view(), name="address"),
]