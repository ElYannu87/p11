from django.test import TestCase
import unittest.mock as u
from io import StringIO
from django.core.management import call_command
from openfoodfacts.api import Api
from openfoodfacts.productparser import ProductParser
# Create your tests here.
"""
Test class for custom Django command
"""


class TestCommand(TestCase):
    """
    This class contains tests about the custom command
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
        pass

    @u.patch('openfoodfacts.management.commands.fill_database.Product')
    @u.patch('openfoodfacts.management.commands.fill_database.Product')
    def test_command_fill_datatabase_output(self, CategoryMock, ProductMock):

        CategoryMock.objects.fill_categories.return_value = True
        ProductMock.objects.fill_products.return_value = True
        out = StringIO()
        call_command('fill_database', stdout=out)
        self.assertIn('Commande effectuée avec succès', out.getvalue())


"""
Test class for Api class
"""


class TestApi(TestCase):
    """
    This class contains tests about API class
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
        self.api = Api()

    @u.patch('builtins.open')
    @u.patch('json.load')
    def test_get_categories_list_from_json_return_list(self, mock_load, mock_json):
        list_json = [
            {
                "category": "Produits laitiers",
                "sub-category": ["Laits", "Beurres", "Boissons lactées", "Fromages"]
            },

            {
                "category": "Boissons",
                "sub-category": ["Sodas", "Boissons au thé", "Boissons énergisantes"]
            }]

        mock_load.return_value = mock_load.return_value = list_json
        self.assertEqual(self.api.get_categories_list_from_json(), list_json)

    @u.patch('openfoodfacts.api.Api.retrieve_informations_from_products')
    @u.patch('requests.Response')
    @u.patch('requests.get')
    @u.patch('builtins.open')
    @u.patch('json.load')
    def test_get_request_response_from_api_works(self, mock_load, mock_open,
                                                 mock_requests_get, MockResponse, mock_retrieve):
        list_json = [
            {
                "category": "Produits laitiers",
                "sub-category": ["Laits", "Beurres", "Boissons lactées", "Fromages"]
            }
        ]

        mock_load.return_value = list_json
        # {"products" : [{"_id" : 123, "product_name" : "Lactel"}]}
        mock_requests_get.return_value = MockResponse
        MockResponse.status_code = 200
        MockResponse.json.return_value = {
            "products": [{"_id": 123, "product_name": "Lactel"}]}
        mock_retrieve.return_value = [{"_id": 123, "product_name": "Lactel"}]
        self.assertEqual(self.api.get_request_response_from_api(), {
            "Laits": [{"_id": 123, "product_name": "Lactel"}],
            "Beurres": [{"_id": 123, "product_name": "Lactel"}],
            "Boissons lactées": [{"_id": 123, "product_name": "Lactel"}],
            "Fromages": [{"_id": 123, "product_name": "Lactel"}],
        })

    def test_retrieve_informations_from_product(self):
        products_list = [
            {"_id": "123",
             "donnee_inutile": "valeur",
             "nutrition_grades": "a",
             "product_name": "lactel",
             "url": "www.test.com",
             "brands": "lactalis",
             "nutriments": {"nutrition-score-fr": "5"},
             "image_url": "www.test-image.com",
             "image_nutrition_url": "www.test-nutrition-url"
             },

            {"_id": "1234",
             "donnee_inutile": "valeur",
             "nutrition_grades": "b",
             "product_name": "lactel-bio",
             "url": "www.test.com",
             "brands": "lactalis-bio",
             "nutriments": {"nutrition-score-fr": "3"},
             "image_url": "www.test-image.com",
             "image_nutrition_url": "www.test-nutrition-url"
             }
        ]

        parsed = [{"_id": "123",
                   "nutrition_grades": "a",
                   "product_name": "lactel",
                   "url": "www.test.com",
                   "brands": "lactalis",
                   "nutrition-score-fr": "5",
                   "image_url": "www.test-image.com",
                   "image_nutrition_url": "www.test-nutrition-url"
                   },
                  {"_id": "1234",
                   "nutrition_grades": "b",
                   "product_name": "lactel-bio",
                   "url": "www.test.com",
                   "brands": "lactalis-bio",
                   "nutrition-score-fr": "3",
                   "image_url": "www.test-image.com",
                   "image_nutrition_url": "www.test-nutrition-url"
                   }]
        self.assertEqual(
            self.api.retrieve_informations_from_products(products_list),
            parsed)


"""
Test class for ProductParser class
"""


class TestProductParser(TestCase):
    """
    This class contains tests about ProductParser class
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
        self.product_parser = ProductParser()

    def test_separate_brands_separe_each_brand_if_multiples_brands(self):
        self.assertEqual(self.product_parser.separate_brands(
            "Coca Cola, Nike, Sprite"), "Coca Cola")

    def test_separate_brands_works_if_one_brand(self):
        self.assertEqual(self.product_parser.separate_brands(
            "Coca Cola"), "Coca Cola")

    def test_check_if_empty_values_return_true_if_empty_values(self):
        product = {"_id": "", "product_name": "Coca zero",
                   "brands": "Coca cola"}
        self.assertIs(self.product_parser.check_if_empty_values(product), True)

    def test_check_if_empty_values_return_False_if_not_empty_values(self):
        product = {"_id": "123", "product_name": "Coca zero",
                   "brands": "Coca cola"}
        self.assertIs(
            self.product_parser.check_if_empty_values(product), False)
