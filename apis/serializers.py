from rest_framework import serializers

from pages.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for the Product model and API"""
    category = serializers.StringRelatedField()

    class Meta:
        fields = (
            "id",
            "name",
            "category",
            "price",
            "stock_quantity",
            "link",
        )
        read_only_fields = ["id"]
        model = Product


class ProductDetailSerializer(ProductSerializer):
    """Serializer for product detail view"""
    class Meta:
        fields = ProductSerializer.Meta.fields + ("description",)
        model = Product
