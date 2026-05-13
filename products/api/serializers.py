from rest_framework import serializers

from ..models import Category,Product,ProductVariant,ProductImage

class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "parent",
            "children"
        ]

    def get_children(self, obj):
        children = obj.children.all()

        return CategorySerializer(children,many=True).data
    

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = [
            "id",
            "image",
            "is_primary",
        ]

class ProductVariantSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True,read_only=True)

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "sku",
            "color",
            "size",
            "price",
            "stock",
            "is_active",
            "images"
        ]

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    variants = ProductVariantSerializer(many=True,read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "thumbnail",
            "category",
            "variants",
            "is_active",
            "created_at",
            "updated_at",
        ]
