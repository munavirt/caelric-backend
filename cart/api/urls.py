from django.urls import path

from .views import CartView,AddToCartView, IncreaseCartItemView, DecreaseCartItemView, RemoveCartItemView


urlpatterns = [
    path("",CartView.as_view(),name="cart"),
    path("add/",AddToCartView.as_view(),name="add-to-cart"),
    path("increase/<int:item_id>/",IncreaseCartItemView.as_view(),name="increase-cart-item"),
    path("decrease/<int:item_id>/",DecreaseCartItemView.as_view(),name="decrease-cart-item"),
    path("remove/",RemoveCartItemView.as_view,name="remove-cart-item")
]