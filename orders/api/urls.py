from django.urls import path

from .views import AddressListCreateView,OrderListView,OrderDetailView,CreateOrderView

urlpatterns = [
    path("addresses/",AddressListCreateView.as_view(),name="address-list-create"),
    path("",OrderListView.as_view(),name="order-list"),
    path("<int:id>/",OrderDetailView.as_view(),name="order-detail"),
    path("create/",CreateOrderView.as_view(),name="create-order")
]