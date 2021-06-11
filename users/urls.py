from django.urls import path, re_path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('register/', views.sign_up, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    url(
        r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate,
        name='activate'
    ),
]
