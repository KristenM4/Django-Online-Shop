from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from pages.models import Product, Category
import os
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class SiteVisitorTest(StaticLiveServerTestCase):
    """
    This user story will test the site's main functionalities, such as browsing products
    and adding products to the cart.

    Requires: selenium, geckodriver, and the firefox browser.
    """

    def setUp(self):
        self.browser = webdriver.Firefox()
        category_1 = Category.objects.create(name="first_category")
        product_1 = Product.objects.create(
            name="first product",
            price=9.99,
            image="img_link",
            description="this is our first product",
            stock_quantity=5,
            discount=.00,
            category=category_1,
            slug="first-product",
        )
    
    def tearDown(self):
        self.browser.quit()
    
    def test_can_browse_products_and_see_product_details_page(self):

        # A new visitor, Agnes, has heard about our website, an online shop named The Sea Wolf, 
        # from social media and wants to check it out
        self.browser.get(self.live_server_url)

        # She sees the shop's name in the title and header
        self.assertIn("The Sea Wolf", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("The Sea Wolf", header_text)

        # Agnes sees the first product displayed on the home page
        products = self.browser.find_elements(By.CLASS_NAME, "product_card")
        self.assertEqual(len(products), 1)
        first_product = products[0]

        # She clicks on the product and is taken to the product's detail page
        first_product.click()
        self.assertTemplateUsed("detail.html")
        product_name = self.browser.find_element(By.CLASS_NAME, "fw-bolder")
        self.assertEqual(product_name.text, "first product")

        # Using the navbar, Agnes goes to the All Products page