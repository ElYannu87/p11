from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('legal_notices', views.legal_notices, name="legal_notices"),
    path('contact', views.contact, name='contact')
]
