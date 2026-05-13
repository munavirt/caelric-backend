from rest_framework import generics
from rest_framework.permissions import AllowAny

from ..models import Category,Product

from .serializers import ProductSerializer,CategorySerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(parent=None)

    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    queryset = Product.objects.filter(is_active=True).prefetch_related("variants","variants_images")

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True).prefetch_related("variants","images","category")

    serializer_class = ProductSerializer
    lookup_field = "slug"

    permission_classes = [AllowAny]
