from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

from products.models import Product

# Create your views here.


def complete(request):
    """
    This view returns a json response wich is a list of product names
    """
    searched_term = request.GET.get("term")
    products = Product.objects.get_products_by_term(searched_term)
    products = [product.product_name + " " +
                product.brand for product in products][:10]
    return JsonResponse(products, safe=False)


def search_products(request):
    """
    This view searches product names that match with a specific term
    """
    try:
        searched_term = request.GET["p"].strip()
    except KeyError:
        return redirect('/')
    if searched_term == "":
        return redirect('/')
    products_possible = Product.objects.get_products_by_term(searched_term)[:9]
    return render(request, 'search/products_searched.html',
                  {"products": products_possible})


def search_products_post(request):
    """
    This view receives the term that the user has written into the 'search bar'
    """
    if request.method == "POST":
        searched_term = request.POST['term'].strip()
        if searched_term == "":
            return redirect('/')

        return redirect('/search?p={}'.format(searched_term))

    else:
        return redirect('/')


def substitutes_products(request, product_id):
    """
    This view search potential substitutes of a product and
    renders this list of substitutes
    """
    product = get_object_or_404(Product, barcode=product_id)
    set_of_substitutes = product.category.product_set.filter(
        nutrition_score__lt=product.nutrition_score).order_by('nutrition_score')[:9]
    return render(request, 'search/substitutes.html',
                  {'product': product, 'substitutes': set_of_substitutes})
