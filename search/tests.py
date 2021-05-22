
from django.test import TestCase, Client
from products.models import Product, Category

# Create your tests here.


class SearchViewTest(TestCase):
    """
    This class contains tests of views of 'users' application
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
        self.category = Category.objects.create(
            name="Pâtes à tartiner", parent_category=None)
        Product.objects.create(barcode="1234",
                               product_name="Chocolat au lait",
                               brand="Milbona",
                               url_page="www.test.com",
                               image_url="www.image-test.com",
                               image_nutrition_url="www.nut-image.com",
                               nutrition_grade="C",
                               nutrition_score=12,
                               category=self.category)
        Product.objects.create(barcode="12345",
                               product_name="Choconot",
                               brand="trista",
                               url_page="www.test.com",
                               image_url="www.image-test.com",
                               image_nutrition_url="www.nut-image.com",
                               nutrition_grade="D",
                               nutrition_score=15,
                               category=self.category)
        Product.objects.create(barcode="123456",
                               product_name="pure beurre",
                               brand="trista",
                               url_page="www.test.com",
                               image_url="www.image-test.com",
                               image_nutrition_url="www.nut-image.com",
                               nutrition_grade="D",
                               nutrition_score=17,
                               category=self.category)

    def test_search_products_returns_a_list_of_products(self):
        response = self.client.get('/search/?p=cho')
        results = response.context['products']
        self.assertTrue(all(str(a) == b for a, b in zip(
            results, ["Chocolat au lait", "Choconot"])))

    def test_search_products_post_redirects_user(self):
        response = self.client.post(
            '/search/post', {"term": "chocolat"}, follow=True)
        self.assertEqual(response.status_code, 200)
        # we check if user is redirected to the right url
        self.assertIn(('/search?p=chocolat', 302), response.redirect_chain)

    def test_substitutes_products_return_a_good_list_of_potential_substitutes(self):
        response = self.client.get('/search/12345/substitutes')
        self.assertEqual(response.status_code, 200)
        results = response.context['substitutes']
        self.assertTrue(
            all(str(a) == b for a, b in zip(results, ["Chocolat au lait"])))

    def test_substitutes_products_return_404_if_product_to_substitute_doesnt_exists(self):
        # this product is not in database
        response = self.client.get('/search/11112241553/substitutes')
        self.assertEqual(response.status_code, 404)