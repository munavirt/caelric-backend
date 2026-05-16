from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Address, Order, OrderItem

from .serializers import AddressSerializer, OrderSerializer, CreateOrderSerializer

from cart.models import Cart

class AddressListCreateView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("items")
    

class OrderDetailView(generics.GenericAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    lookup_field = "id"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("items")

    
class CreateOrderView(generics.GenericAPIView):
    serializer_class = CreateOrderSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_excepiton=True)
        address_id = serializer.validated_data["address_id"]

        try:
            address = Address.objects.get(id=address_id,user=request.user)

        except Address.DoesNotExist:
            return Response({"error":"Address not found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            cart = Cart.objects.get(user=request.user)

        except Cart.DoesNotExist:
            return Response({"error":"cart is empty"},status=status.HTTP_400_BAD_REQUEST)
        
        cart_items = cart.items.all()

        if not cart_items.exists():
            return Response({"error" : "cart it empty"},status=status.HTTP_400_BAD_REQUEST)
        
        total_price = sum(item.subtotal for item in cart_items)

        order = Order.objects.create(user=request.user,address=address,total_price=total_price)

        for item in cart_items:
            OrderItem.objects.create(
                order = order,
                product_variant = item.product_variant,
                quantity = item.quantity,
                price = item.product_variant.price,
            )

            variant = item.product_variant
            vriant.stock -= item.quantity
            variant.save()

        cart_items.delete()

        return Response(OrderSerializer(order).data,status=status.HTTP_201_CREATED)
        

