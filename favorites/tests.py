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

    def test_export_favorites_from_user_returns_favorites_into_a_file(self):
        response = self.client.get('/favorite/export')
        # the name of the file has to be 'favorites' + name of user
        correct_filename = '"favorites_Michello.json"' in response.get("Content-Disposition")
        self.assertIs(correct_filename, True)
        json_obj = json.loads(response.content)
        user_favorite = Favorite.objects.all()[0]
        fav_infos = {}
        fav_infos["Code barre produit"] = user_favorite.product.barcode
        fav_infos["Nom produit"] = user_favorite.product.product_name
        fav_infos["Code barre substitut"] = user_favorite.substitute.barcode
        fav_infos["Nom substitut"] = user_favorite.substitute.product_name
        fav_infos["Marque substitut"] = user_favorite.substitute.brand
        fav_infos["Marque produit"] = user_favorite.product.brand
        # we checks if informations inside file is the same has informations about user's favorites
        self.assertEqual(json_obj, [fav_infos])

    def test_import_json_file_adds_favorites(self):
        p3 = Product.objects.create(barcode="123456",
                                    product_name="Lait3",
                                    brand="gandia +",
                                    url_page="www.test.com",
                                    image_url="www.image-test.com",
                                    image_nutrition_url="www.nut-image.com",
                                    nutrition_grade="A",
                                    nutrition_score=1,
                                    category=self.cat)
        file_content = b'[{"test": "123"}, {"Code barre produit" :"1234", "Code barre substitut" : "123456"}]'
        imported_file = SimpleUploadedFile("my_favs.json", file_content, content_type="application/json")
        # we simulate an upload of a json file with some content inside
        response = self.client.post("/favorite/import", {"imported_file" : imported_file}, follow=True)
        # if everything goes well, a new favorite should be added
        expected = ["Lait1 remplacé par Lait2", "Lait1 remplacé par Lait3"]
        user_favorites = Favorite.objects.get_favorites_from_user(self.user1)
        self.assertTrue(
            all(str(a) == b for a, b in zip(user_favorites, expected)))
        # we make sure good messages are delivered
        for message in response.context['messages']:
            self.assertIn(str(message), ["le ou les favoris suivants ont été ajoutés : produit 1234/ substitut 123456, ",
                                    "au moins un couple produit/substitut n'a pas été ajouté car sa structure n'est pas correcte"])