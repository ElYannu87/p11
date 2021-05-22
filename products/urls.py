from django.urls import path
from . import views

urlpatterns = [
    path('<pk>', views.DetailProduct.as_view(), name="detail"),
]