from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Product, Category, Review


class PagesTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Creating a user, category, product, and review
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@email.com",
            password="testing123",
            first_name="Test",
            last_name="User",
            date_of_birth="2000-01-01",
        )

        cls.category = Category.objects.create(name="Categories")

        cls.product = Product.objects.create(
            name="New Product",
            price="10.99",
            image="some_image.jpg",
            description="This is a new product",
            stock_quantity=15,
            discount=.00,
            category=cls.category,
            slug="new-product",
        )

        cls.review = Review.objects.create(
            customer=cls.user,
            product=cls.product,
            text="A review for this product.",
            rating="4",
        )


    def test_product_listing(self):
        self.assertEqual(self.product.name, "New Product")
        self.assertEqual(self.product.stock_quantity, 15)
        self.assertEqual(self.product.category, self.category)

    def test_homepage(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "New Product")
        self.assertNotContains(response, "A review for this product")
        self.assertTemplateUsed(response, "home.html")

    def test_aboutpage(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "About Us")
        self.assertTemplateUsed(response, "about.html")

    def test_detailpage(self):
        response = self.client.get(self.product.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "New Product")
        self.assertContains(response, "A review for this product")
        self.assertTemplateUsed(response, "detail.html")

    def test_categorypage(self):
        response = self.client.get(reverse("category", args=[str(self.category)]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Categories")
        self.assertTemplateUsed(response, "category.html")

    def test_apipage(self):
        response = self.client.get(reverse("api-info"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The Sea Wolf API")
        self.assertTemplateUsed(response, "api_info.html")
