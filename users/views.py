from django.shortcuts import render, redirect
from sentry_sdk import capture_message
from .forms import SignUpForm, LoginForm
from .models import User
from django.db.utils import IntegrityError
from django.contrib.auth import login as log, authenticate, logout as out
from django.contrib import messages
import logging
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.core.mail import EmailMessage
# Create your views here.


def sign_up(request):
    """
    This view render sign_up form and allows user to create an account
    (and handle cases where an account already exists etc...)
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password'])
                # until, the user has not activated his account, is_active is False
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = "Activez votre compte PurBeurre"
                # we transform the template into a string
                message = render_to_string('users/acc_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
                })
                # email where to send the activation link
                to_email = form.cleaned_data.get('email')
                # we create the email
                email = EmailMessage(
                        mail_subject, message, to=[to_email]
                )
                email.send() # we send it
                messages.add_message(request, messages.INFO,
                    'Un email vous a été envoyé')
                capture_message("un nouvel utilisateur a été créé : {} avec l'email {}".format(user.username, user.email))
                return redirect('home')
            except IntegrityError:
                return render(request, 'users/register.html', {"form": form, "user_exists": True})

            log(request, user)
            messages.add_message(request, messages.INFO,
                                 'Welcome home, {}'.format(user.username))
            return redirect('home')

    else:  # if request method is "get"
        form = SignUpForm()
    return render(request, 'users/register.html', {"form": form, "user_exists": False})


def login(request):
    """
    This view render login form and allows user to login
    (and handle cases where an account not exists etc...)
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                # if user has not yet activated is account, he cannot login
                if user.is_active is False:
                    messages.add_message(request, messages.INFO,
                        "Votre compte n'est pas encore activé")
                    return redirect('home')
                log(request, user)
                messages.add_message(request, messages.INFO,
                                     'Welcome home, {}'.format(user.username))
                return redirect('home')
            else:
                user_exists = False
                return render(request, 'users/login.html',
                              {"form": form, 'user_exists': user_exists})
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {"form": form, 'user_exists': True})


def logout(request):
    """
    This view allows user to logout
    """
    out(request)
    messages.add_message(request, messages.INFO, 'Revenez vite nous voir !')
    return redirect('home')


def activate(request, uidb64, token):
    """
    This method active user account when he click on the link
    inside the email he received
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        log(request, user)
        messages.add_message(request, messages.INFO,
                                     'Votre compte est bien confirmé')
        capture_message("l'utilisateur {} a activé son compte".format(user.username))
        return redirect('home')
    else:
        return HttpResponse('Activation link is invalid!')