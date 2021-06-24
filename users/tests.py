from django.test import TestCase, Client
from django.core import mail
from django.urls import resolve
from users.forms import LoginForm, SignUpForm
from users.models import User
from django.contrib import auth

# Create your tests here.


class UsersViewTest(TestCase):
    """
    This class contains tests of views of 'users' application
    """
    @classmethod
    def setUpTestData(cls):
        """
        This function is executed once at the beginning of test launching
        """
        pass

    def setUp(self):
        """
        This function is executed each time a new test function is executed
        """
        self.client = Client()
        User.objects.create_user(
            username="Michello", password="1234", email="test@test.com")

    def test_login_view_has_status_200(self):

        response = self.client.get('/user/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_view_get_request(self):
        response = self.client.get('/user/login/')
        self.assertEqual(response.request["REQUEST_METHOD"], "GET")
        self.assertIsInstance(response.context["form"], LoginForm)
        self.assertEqual(response.context['user_exists'], True)

    def test_login_view_post_request(self):
        response = self.client.post(
            '/user/login/', {"username": 'Michel', "password": '1234'})
        self.assertEqual(response.request["REQUEST_METHOD"], "POST")
        self.assertIsInstance(response.context["form"], LoginForm)
        self.assertEqual(response.context['user_exists'], False)

    def test_login_view_post_request_with_a_unkown_user(self):
        response = self.client.post(
            '/user/login/', {"username": 'Michel', "password": '1234'})
        self.assertEqual(response.request["REQUEST_METHOD"], "POST")
        self.assertIsInstance(response.context["form"], LoginForm)
        self.assertEqual(response.context['user_exists'], False)
        self.assertIs(response.context['user'].is_anonymous, True)

    def test_login_view_post_request_wich_log_a_user(self):

        response = self.client.post(
            '/user/login/', {"username": 'Michello', "password": '1234'})
        self.assertEqual(response.request["REQUEST_METHOD"], "POST")
        self.assertEqual(response.status_code, 302)
        user = auth.get_user(self.client)
        self.assertIs(user.is_authenticated, True)

    def test_sign_up_view_has_status_200(self):
        response = self.client.get('/user/register/')
        self.assertEqual(response.status_code, 200)

    def test_login_view_post_request_when_user_exists(self):
        response = self.client.post(
            '/user/register/',
            {"username": 'Michello', "email": "test@test.com", "password": '1234'})
        self.assertEqual(response.request["REQUEST_METHOD"], "POST")
        self.assertIsInstance(response.context["form"], SignUpForm)
        self.assertEqual(response.context['user_exists'], True)
        self.assertIs(response.context['user'].is_authenticated, False)

    def test_login_view_post_request_log_new_user(self):
        response = self.client.post(
            '/user/register/', {"username": 'Michel', "email": "t@test.com", "password": '1234'})
        new_user = User.objects.get(email="t@test.com")
        new_user.is_active = True
        new_user.save()
        response = self.client.post(
            '/user/login/', {"username": 'Michel', "password": '1234'})
        self.assertEqual(response.request["REQUEST_METHOD"], "POST")
        user = auth.get_user(self.client)
        self.assertIs(user.is_authenticated, True)

    def test_login_view_post_request_log_new_user_redirects(self):
        response = self.client.post(
            '/user/register/', {"username": 'Michel', "email": "t@test.com", "password": '1234'})
        self.assertEqual(response.status_code, 302)

    def test_logout_view_logout_user_from_session(self):
        self.client.login(username='Michello', password='1234')
        user = auth.get_user(self.client)
        self.assertIs(user.is_authenticated, True)
        self.client.post('/user/logout/')
        user = auth.get_user(self.client)
        self.assertIs(user.is_authenticated, False)

    def test_email_is_send_when_a_new_user_create_an_account(self):
        response = self.client.post(
            '/user/register/', {"username": 'Michel', "email": "t@test.com", "password": '1234'})
        #when testing, django "sends" email to a list named "outbox"
        #check if an email has been send
        self.assertEqual(len(mail.outbox), 1)
        #we check if the mail is the mail to activate user account
        self.assertEqual(mail.outbox[0].subject,"Activez votre compte PurBeurre")
        #we check if email has been send to the  user's email
        self.assertEqual(mail.outbox[0].to[0],"t@test.com")

    def test_is_active_is_false_when_a_new_user_create_an_account(self):
        response = self.client.post(
            '/user/register/', {"username": 'Michel', "email": "t@test.com", "password": '1234'}, follow=True)
        new_user = User.objects.get(email="t@test.com")
        self.assertIs(new_user.is_active, False)
        #check if the right message is displayed
        for message in response.context['messages']:
            self.assertEqual(str(message), "Un email vous a été envoyé")
        
    def test_user_cannot_login_until_is_account_is_validated(self):
        #new user create an account but has not yet validated is account
        self.client.post(
            '/user/register/', {"username": 'Michel', "email": "t@test.com", "password": '1234'})
        # user try to login
        response = self.client.post(
            '/user/login/', {"username": 'Michel', "password": '1234'}, follow=True)
        session_user = auth.get_user(self.client)
        # check if user is not authenticated
        self.assertIs(session_user.is_authenticated, False)
        #check if the right message is displayed
        for message in response.context['messages']:
            self.assertIn(str(message), ["Un email vous a été envoyé","Votre compte n'est pas encore activé"])

    def test_activate_view_change_is_active_attribute_to_true(self):
        response = self.client.post(
            '/user/register/', {"username": 'Michel', "email": "t@test.com", "password": '1234'})
        new_user = User.objects.get(email="t@test.com")
        # make sure the user is created but his account is not active
        self.assertIs(new_user.is_active, False)
        min_index = mail.outbox[0].body.find("/user/")
        route =  mail.outbox[0].body[min_index:]
        max_index = len(mail.outbox[0].body)
        route = route[:max_index-2]
        #we simulate that the user clicks on the link inside the email
        response = self.client.get(route, follow=True)
        new_user = User.objects.get(email="t@test.com")
        #if everything is works, the account of user is now active
        self.assertIs(new_user.is_active, True)
        #we checks the messages
        for message in response.context['messages']:
            self.assertIn(str(message), ["Un email vous a été envoyé","Votre compte est bien confirmé"])


    def test_name_of_route_to_login_is_login(self):
        """
        We will check if the name of the route wich leads to the login view
        is 'login'
        """
        resolver = resolve('/user/login/')
        self.assertEqual(resolver.url_name, 'login')

    def test_name_of_route_to_register_is_signup(self):
        """
        We will check if the name of the route wich leads to the register view
        is 'signup'
        """
        resolver = resolve('/user/register/')
        self.assertEqual(resolver.url_name, 'signup')

    def test_name_of_route_to_logout_is_logout(self):
        """
        We will check if the name of the route wich leads to the logout view
        is 'logout'
        """
        resolver = resolve('/user/logout/')
        self.assertEqual(resolver.url_name, 'logout')