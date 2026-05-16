from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from ..models import Cart, CartItem

from .serializers import CartItemSerializer, CartSerializer, AddToCartSerializer

from products.models import ProductVariant

class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user = self.request.user)
        return cart
    

class AddToCartView(generics.GenericAPIView):
    serializer_class = AddToCartSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data = request.data)

        serializer.is_valid(raise_exception=True)
        variant_id = serializer.validated_data["variant_id"]
        quantity = serializer.validated_data["quantity"]

        try:
            variant = ProductVariant.objects.get(id=variant_id,is_active=True)

        except ProductVariant.DoesNotExist:
            return Response({"error" : "Product variant not found"},status=status.HTTP_404_NOT_FOUND)

        
        cart, created = Cart.objects.get_or_create(
            user = request.user
        )

        cart_item,created = CartItem.objects.get_or_create(cart=cart,product_variant=variant)

        if not created:
            create_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()

        return Response({"message":"Item added to cart"},status=status.HTTP_200_OK)
    

class IncreaseCartItemView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, item_id):
        try:
            cart_item = CartItem.objects.get(id=item_id,cart_user=request.user)

        except CartItem.DoesNotExist:
            return Response({"error" : "Cart item not found"},status=status.HTTP_404_NOT_FOUND)
        
        cart_item.quantity +=1
        
        cart_item.save()

        return Response({"message" : "quantity increased"})
    

class DecreaseCartItemView(generics.GenericAPIView):
    permission_classes  = [IsAuthenticated]

    def post(self, request, item_id):
        try:
            cart_item = CartItem.objects.get(id=item_id, cart_user=request.user)

        except CartItem.DoesNotExist:
            return Response({"error" : "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if cart_item.quantity>1:
            cart_item.item -=1
            cart_item.save()

        else:
            cart_item.delete()

        return Response({"message": "Quantity Decreased"})
    

class RemoveCartItemView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    lookup_url_kwarg = "item_id"

    def get_queryset(self):
        return CartItem.objects.filter(cart_user = self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        self.perform_destroy(instance)
        return Response({"message":"item removed from cart"},status=status.HTTP_200_OK)
    
    