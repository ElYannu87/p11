"""
This module contains tests of app 'favorites'
"""
from django.test import TestCase, Client
from users.models import User
from products.models import Product, Category
from .models import Favorite
from django.contrib.auth import logout


# Create your tests here.

class TestFavorites(TestCase):
    def test_favorite_match(self):
        "test to check if productname is correct"
        self.category = Category.objects.create(name="Lait", parent_category=None)
        self.produit1 = Product.objects.create(barcode="1234",
                                         product_name="Lait1",
                                         brand="Lactel",
                                         url_page="www.test.com",
                                         image_url="www.image-test.com",
                                         image_nutrition_url="www.nut-image.com",
                                         nutrition_grade="B",
                                         nutrition_score=5,
                                         category=self.category
                                )
        self.produit2 = Product.objects.create(barcode="1235",
                                         product_name="Lait2",
                                         brand="Gandia",
                                         url_page="www.test.com",
                                         image_url="www.image-test.com",
                                         image_nutrition_url="www.nut-image.com",
                                         nutrition_grade="A",
                                         nutrition_score=6,
                                         category=self.category
                                )
        self.yannu = User.objects.create_user('Yannu', 'yannu@test.com', '1111')
        Favorite.objects.create(user=self.yannu, product=self.produit1, substitute=self.produit2)
        fav_of_yannu = Favorite.objects.get_favorites_from_user(self.yannu)
        self.assertQuerysetEqual((fav_of_yannu[0].product.product_name, fav_of_yannu[0].substitute.product_name), ("Lait1", "Lait2"),ordered=False, transform=str)
