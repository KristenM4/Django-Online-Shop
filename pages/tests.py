from django.test import TestCase
from .models import Product, Category

# Create your tests here.

class ProductAndCategoryModelsTest(TestCase):
    def test_saving_and_retrieving_products(self):
        category_ = Category(name="Some category")
        category_.save()
        product = Product(
            name="New Product",
            price="10.99",
            image="some_image.jpg",
            description="This is a new product",
            stock_quantity=15,
            discount=.00,
            category=category_,
        )
        product.save()

        new_product = Product.objects.all()[0]
        self.assertEqual(new_product.name, "New Product")
        self.assertEqual(new_product.category, category_)


class HomePageTest(TestCase):

    def test_uses_correct_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")
