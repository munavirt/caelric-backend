from rest_framework import serializers

from ..models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product_variant.product.name",read_only=True)
    color = serializers.CharField(source="product_variant.size",read_only=True)
    price = serializers.DecimalField(source="product_variant.price",max_digits=10,decimal_places=2,read_only=True)

    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product_variant",
            "product_name",
            "color",
            "size",
            "price",
            "quantity",
            "subtotal",

        ]

    def get_subtotal(self, obj):
        return obj.subtotal
    

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True,read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart

        fields = [
            "id",
            "items",
            "total_price"
        ]

    def get_total_price(self, obj):
        return sum(item.subtotal for item in obj.items.all())
    

class AddToCartSerializer(serializers.Serializer):
    variant_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1)