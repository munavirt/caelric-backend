from rest_framework import serializers

from ..models import Address,Order,OrderItem

from cart.models import Cart


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address

        fields = [
            "id",
            "full_name",
            "phone",
            "address_line_1",
            "address_line_2",
            "city",
            "state",
            "postal_code",
            "country",
            "is_default",
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="prodcut_variant.product.name",read_only=True)
    color = serializers.CharField(source="product_variant.color",read_only=True)
    size = serializers.CharField(source="product_variant.size",read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product_name",
            "color",
            "size",
            "price",
            "quantity",
            "subtotal",
        ]

    def get_subtotal(self, obj):
        return obj.subtotal
    

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True,read_only=True)
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Order

        fields = [
            "id",
            "status",
            "total_price",
            "address",
            "items",
            "created_at",
        ]

class CreateOrderSerializer(serializers.Serializer):
    address_id = serializers.IntegerField()