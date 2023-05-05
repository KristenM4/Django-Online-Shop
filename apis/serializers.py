from rest_framework import serializers

from pages.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for the Product model and API"""
    class Meta:
        fields = (
            "id",
            "name",
            "category",
            "price",
            "stock_quantity",
        )
        model = Product