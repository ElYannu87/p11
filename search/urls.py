from django.urls import path

from . import views

urlpatterns = [
    path("complete", views.complete, name="complete"),
    path("post", views.search_products_post, name="search_products_post"),
    path("", views.search_products, name="search_products"),
    path("<product_id>/substitutes", views.substitutes_products,
         name="substitutes_product")
]
