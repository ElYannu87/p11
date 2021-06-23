from django.urls import path, re_path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('register/', views.sign_up, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path(
        'activate/<str:uidb64>/<str:token>/',
        views.activate,
        name='activate'
    ),
]
