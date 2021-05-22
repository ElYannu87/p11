from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.db import IntegrityError
from .models import Favorite
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import User
from products.models import Product
from .import_export_favorites import serialize_favorites_from_user as serialize
from .import_export_favorites import find_favorites_from_json, add_favorites_from_json
from .import_export_favorites import file_imported_and_is_json, analyse_fav_to_add

# Create your views here.

# user has to be logged if he want to see favorites


@login_required(login_url='login')
def user_favorites(request):
    """
    Allows a user to see their favorites
    """
    current_user_id = request.session.get("_auth_user_id")
    user = User.objects.get(id=current_user_id)
    user_favorites_set = Favorite.objects.get_favorites_from_user(user)
    return render(request, "favorites/favorites.html", {"favorites":
                                                        user_favorites_set})


@login_required(login_url='login')
def add_favorite(request, product_id, substitute_id):
    """
    Allows a user to save their favorites and to save them into the database
    """
    current_user_id = request.session.get("_auth_user_id")
    user = User.objects.get(id=current_user_id)
    try:
        product, substitute = (Product.objects.get(barcode=product_id),
                               Product.objects.get(barcode=substitute_id))
    except (IntegrityError, Product.DoesNotExist):
        # if the product or substitute doesn't exist
        messages.info(request, "Produit ou substitut inexistant !")
        return redirect('/')
    favorite = Favorite(user=user, product=product, substitute=substitute)
    try:
        favorite.save()
    except IntegrityError:
        # if tuple (product, substitute) is already save as favorite
        messages.info(request, "Ce favori existe déjà !")
        return redirect('/')

    return redirect("user_favorites")


@login_required(login_url='login')
def export_favorites_from_user(request):
    current_user_id = request.session.get("_auth_user_id")
    user = User.objects.get(id=current_user_id)
    json_file = serialize(user)
    response = HttpResponse(json_file, content_type="application/json")
    response['Content-Disposition'] = 'attachement; filename="favorites_{}.json"'.format(user.username)
    return response

@login_required(login_url='login')
def import_json_file(request):
    if request.method == 'POST':
        json_file = file_imported_and_is_json(request)
        if json_file is False:
            return redirect('user_favorites')
        binary_datas = json_file.read()
        fav_list_to_add = find_favorites_from_json(binary_datas)
        fav_list_to_add = analyse_fav_to_add(request, fav_list_to_add)
        if fav_list_to_add is False:
            return redirect('user_favorites')
        results_dtb = add_favorites_from_json(request, fav_list_to_add)
        for info in results_dtb:
            messages.info(request, info)
        return redirect('user_favorites')