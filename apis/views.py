from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from pages.models import Product
from apis.permissions import IsAdminOrReadOnly
from apis.serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer