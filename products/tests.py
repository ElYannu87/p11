from django.test import TestCase, Client
from products.models import Product, Category
from django.db import IntegrityError
from unittest.mock import patch

# Create your tests here.


class ProductsViewTest(TestCase):
    """
    This class contains tests of views of 'product' application
    """

    @classmethod
    def setUpTestData(cls):
        """
        This function is executed once at the beginning of test launching
        """
        pass

    def setUp(self):
        """
        This function is executed each time a new test function is executed
        """
        self.client = Client()
        self.cat = Category.objects.create(name="Lait", parent_category=None)
        Product.objects.create(barcode="1234",
                               product_name="Lait",
                               brand="Lactel",
                               url_page="www.test.com",
                               image_url="www.image-test.com",
                               image_nutrition_url="www.nut-image.com",
                               nutrition_grade="A",
                               nutrition_score=5,
                               category=self.cat)

    def test_view_detail_product_return_response_200_if_product_exists(self):
        response = self.client.get('/product/1234')
        self.assertEqual(response.request["REQUEST_METHOD"], "GET")
        self.assertEqual(response.status_code, 200)

    def test_view_detail_product_response_contains_informations_about_product(self):
        response = self.client.get('/product/1234')
        self.assertContains(response, "Lait")
        self.assertContains(response, "Marque du produit : Lactel")

    def test_view_detail_product_return_response_404_if_product_doesnt_exists(self):
        response = self.client.get('/product/1111111')
        self.assertEqual(response.request["REQUEST_METHOD"], "GET")
        self.assertEqual(response.status_code, 404)


class ProductModelTest(TestCase):
    """
    This class contains tests about Product Model
    """

    @classmethod
    def setUpTestData(cls):
        """
        This function is executed once at the beginning of test launching
        """
        pass

    def setUp(self):
        """
        This function is executed each time a new test function is executed
        """
        self.cat = Category.objects.create(name="Lait", parent_category=None)
        Product.objects.create(barcode="1234",
                               product_name="Lait",
                               brand="Lactel",
                               url_page="www.test.com",
                               image_url="www.image-test.com",
                               image_nutrition_url="www.nut-image.com",
                               nutrition_grade="A",
                               nutrition_score=5,
                               category=self.cat)

    def test_integrity_error_if_product_with_identical_barcode(self):
        with self.assertRaises(IntegrityError):
            Product.objects.create(barcode="1234",
                                   product_name="Laits",
                                   brand="Lactalis",
                                   url_page="www.test123.com",
                                   image_url="www.images-test.com",
                                   image_nutrition_url="www.nuttrition-image.com",
                                   nutrition_grade="B",
                                   nutrition_score=7,
                                   category=self.cat)

    @patch('products.models.Api')
    @patch('json.load')
    @patch('builtins.open')
    def test_custom_manager_method_add_products(self, mock_open, mock_load, MockApi):
        mock_load.return_value = [
            {
                "category": "Produits laitiers",
                "sub-category": ["Lait"]
            }]
        MockApi.return_value = MockApi
        MockApi.get_request_response_from_api.return_value = {"Lait": [
            {"_id": "1111",
             "product_name": "lait de vanille",
             "brands": "lactel",
             "url": "test",
             "image_url": "test",
             "image_nutrition_url": "test",
             "nutrition_grades": "A",
             "nutrition-score-fr": 0,
             },
            {"_id": "1112",
             "product_name": "lait de vache",
             "brands": "lactalis",
             "url": "test",
             "image_url": "test",
             "image_nutrition_url": "test",
             "nutrition_grades": "B",
             "nutrition-score-fr": 2,
             }
        ]}

        Product.objects.fill_products()
        self.assertQuerysetEqual(Product.objects.all(),
                                 set(["Lait", "lait de vanille", "lait de vache"]),
                                 ordered=False, transform=str)


class CategoryModelTest(TestCase):
    """
    This class contains tests about Category model
    """

    @classmethod
    def setUpTestData(cls):
        """
        This function is executed once at the beginning of test launching
        """
        pass

    def setUp(self):
        """
        This function is executed each time a new test function is executed
        """
    @patch('json.load')
    @patch('builtins.open')
    def test_custom_manager_method_adds_categories(self, mock_open, mock_load):
        mock_load.return_value = [
            {
                "category": "Produits laitiers",
                "sub-category": ["Laits", "Beurres", "Boissons lactées", "Fromages"]
            },

            {
                "category": "Boissons",
                "sub-category": ["Sodas", "Boissons au thé", "Boissons énergisantes"]
            }
        ]
        Category.objects.fill_categories()
        self.assertQuerysetEqual(Category.objects.all(),
                                 set(["Produits laitiers", "Laits", "Beurres",
                                      "Boissons lactées", "Fromages", "Boissons",
                                      "Sodas", "Boissons au thé", "Boissons énergisantes"]),
                                 ordered=False, transform=str)
