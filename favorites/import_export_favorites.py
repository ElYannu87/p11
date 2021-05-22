from .models import Favorite
from django.db import IntegrityError, transaction
from users.models import User
from products.models import Product
from json import dumps, loads, JSONDecodeError
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages


def serialize_favorites_from_user(user):
    user_favorites = Favorite.objects.get_favorites_from_user(user)
    favorites_list = []

    for fav in user_favorites:
        fav_dict = {}
        fav_dict["Code barre produit"] = fav.product.barcode
        fav_dict["Nom Produit"] = fav.product.product_name
        fav_dict["Marque Produit"] = fav.product.brand
        fav_dict["Code barre substitut"] = fav.substitute.barcode
        fav_dict["Nom substitut"] = fav.substitute.product_name
        fav_dict["Marque substitut"] = fav.substitute.brand
        favorites_list.append(fav_dict)

    return dumps(favorites_list, indent=4, ensure_ascii=False).encode('utf8')

def find_favorites_from_json(raw_data):
    try:
        json_datas = loads(raw_data)
    except JSONDecodeError:
        return (False, "Fichier Json non valide")
    skipped_datas = False
    if type(json_datas) is not list:
        return (False, "La structure du fichier json n'est pas valide")
    fav_barcode_list = []
    for favorite_json in json_datas:
        if type(favorite_json) is not dict:
            return (False, "La structure du fichier json n'est pas valide")
        try:
            product = favorite_json["Code barre produit"]
            substitute = favorite_json["Code barre substitut"]
        except KeyError:
            skipped_datas = True
            continue
        fav_barcode_list.append((product, substitute))
    if skipped_datas is True:
        return (True, "Au moins une paire produit/substitut n'a pas été ajouté car sa structure n'est pas valide", fav_barcode_list)
    return fav_barcode_list


def generate_messages(products_added, products_already_saved, products_not_found):
    results = []
    if len(products_added) > 0:
        sentence : "le ou les favrosi suivants ont été ajoutés :"
        for added in products_added:
            sentence += "produit {}/ substitut {}, ".format(added[0], added[1])
        results.append(sentence)
    if len(products_already_saved) > 0:
        sentence : "le ou les favoris suivants ont déjà été enregistrés en tant que favoris : "
        for existed in products_already_saved:
            sentence += "produit {}/ substitut {}, ".format(added[0], existed[1])
        results.append(sentence)
    if len(products_not_found) > 0:
        sentence = "le ou les paires de produits/substituts n'ont pas été trouvé dans la base de données : "
        for not_found in products_not_found:
            sentence += "produit {}/ substitut {}, ".format(added[0], not_found[1])
        results.append(sentence)
    return results

def add_favorites_from_json(request, fav_list):
    current_user_id = request.session.get("auth_user_id")
    user = User.objects.get(id=current_user_id)
    products_not_found = []
    products_already_saved = []
    products_added = []
    for fav in fav_list:
        try:
            with transaction.atomic():
                product, substitute = (Product.objects.get(barcode=fav[0]),
                                Product.objects.get(barcode=fav[1]))
        except Product.DoesNotExist:
            products_not_found.append(fav)
            continue
        favorite = Favorite(user=user, product=product, substitute=substitute)
        try:
            with transaction.atomic():
                favorite.save()
                products_added.append(fav)
        except IntegrityError:
            products_already_saved.append(fav)
    return generate_messages(products_added, products_already_saved, products_not_found)


def file_imported_and_is_json(request):
    try:
        json_file = request.FILES['imported_file']
    except (MultiValueDictKeyError, KeyError):
        messages.error(request, "Le fichier n'a pas été uploadé")
        return False
    if not json_file.name.endswith(".json"):
        messages.error(request, "Le fichier uploadé n'est pas un fichier json")
        return False
    return json_file

def analyse_fav_to_add(request, fav_list_to_add):
    if type(fav_list_to_add) is tuple:
        if fav_list_to_add[0] is False:
            messages.error(request, fav_list_to_add[1])
            return False
        else:
            messages.warning(request, fav_list_to_add[1])
            fav_list_to_add = fav_list_to_add[2]
    if len(fav_list_to_add) == 0:
        messages.error(request,"Aucun produit à ajouter")
        return False
    return fav_list_to_add
