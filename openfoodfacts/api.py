import sys
import requests
import json

from . import productparser


class Api:
    """
    This class handles the interactions with the openfoodfacts API
    """
    KEYS = [
        "_id", "nutrition_grades",
        "product_name", "url", "brands",
        ("nutriments", "nutrition-score-fr"),
        "image_url", "image_nutrition_url"
    ]

    def __init__(self):
        self.products_list = {}
        self.checker = productparser.ProductParser()

    def get_categories_list_from_json(self):
        """
        We retrieve informations from a json file
        """
        with open("static/json/categories.json", "r", encoding="utf8") as file:
            categories_list = json.load(file)

        return categories_list

    def get_request_response_from_api(self):
        """
        get HTTP response from OpenFoodFact's API
        """
        categories_list = self.get_categories_list_from_json()
        products_dict = {}
        for category_dict in categories_list:
            for sub_category in category_dict["sub-category"]:
                # we make get request for each sub-category
                HTTP_LINK = ("https://be-fr.openfoodfacts.org/cgi/search.pl?search_simple=1"
                             "&action=process&tagtype_0=categories&tag_contains_0=contains&tag_0={}"
                             "&sort_by=unique_scans_n&page_size=30&json=1")
                try:
                    request = requests.get(HTTP_LINK.format(sub_category))
                    if request.status_code != 200:
                        raise requests.ConnectionError

                except requests.ConnectionError:
                    print(("une erreur est survenue "
                           "lors de l'envoi/la récupération"
                           "de la requête HTTP"))
                    sys.exit()
                request = request.json()["products"]
                # we retrieve informations about products of a sub-category
                parsed_products = self.retrieve_informations_from_products(
                    request)
                products_dict[sub_category] = parsed_products
        return products_dict

    def retrieve_informations_from_products(self, products_list):
        """
        Retrieving the  informations we need about each product
        """
        products_list_parsed = []
        for product in products_list:
            product_values = {}
            try:
                for key in self.KEYS:
                    if type(key) is tuple:
                        product_values[key[1]] = product[key[0]][key[1]]
                    else:
                        product_values[key] = product[key]

                product_values["brands"] = self.checker.separate_brands(
                    product_values["brands"])

            except KeyError:
                continue

            if not self.checker.check_if_empty_values(product_values):
                products_list_parsed.append(product_values)
        return products_list_parsed
