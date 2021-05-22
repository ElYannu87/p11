from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, "pages/home.html")


def legal_notices(request):
    return render(request, 'pages/legal_notices.html')


def contact(request):
    return render(request, 'pages/contact.html')
