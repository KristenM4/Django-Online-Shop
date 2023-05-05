from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from pages.models import Product, Category
from apis.serializers import ProductSerializer


PRODUCTS_URL = reverse("products:products-list")


def product_detail_url(product_id):
    return reverse("products:products-detail", args=[product_id])


class ProductApiTests(TestCase):
    """Tests for the Products API"""
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.category = Category.objects.create(
            name="Hats",
        )
        cls.product = Product.objects.create(
            name="Baseball Cap",
            price="9.99",
            image="http://image.com",
            description="A nice hat",
            stock_quantity=8,
            discount=.00,
            category=cls.category,
        )

    def test_product_model(self):
        self.assertEqual(self.product.name, "Baseball Cap")
        self.assertEqual(self.product.price, "9.99")
        self.assertEqual(self.product.category, self.category)

    def test_retrieve_products_list(self):
        res = self.client.get(PRODUCTS_URL)
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_product_detail(self):
        url = product_detail_url(self.product.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["name"], self.product.name)
