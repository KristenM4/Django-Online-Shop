from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from pages.models import Product
from apis.permissions import IsAdminOrReadOnly
from apis.serializers import ProductDetailSerializer, ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

    def get_serializer_class(self):
        """Return the serializer class for request"""
        if self.action == "list":
            return ProductSerializer

        return self.serializer_class