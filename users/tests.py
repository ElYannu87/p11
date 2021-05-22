from django.test import TestCase, Client
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
            {"username": 'Michello', "email": "test@test.com",
             "password": '1234'})
        self.assertEqual(response.request["REQUEST_METHOD"], "POST")
        self.assertIsInstance(response.context["form"], SignUpForm)
        self.assertEqual(response.context['user_exists'], True)
        self.assertIs(response.context['user'].is_authenticated, False)

    def test_login_view_post_request_log_new_user(self):
        response = self.client.post(
            '/user/register/', {"username": 'Michel', "email": "t@test.com",
                                "password": '1234'})
        self.assertEqual(response.request["REQUEST_METHOD"], "POST")
        user = auth.get_user(self.client)
        self.assertIs(user.is_authenticated, True)

    def test_login_view_post_request_log_new_user_redirects(self):
        response = self.client.post(
            '/user/register/', {"username": 'Michel', "email": "t@test.com",
                                "password": '1234'})
        self.assertEqual(response.status_code, 302)

    def test_logout_view_logout_user_from_session(self):
        self.client.login(username='Michello', password='1234')
        user = auth.get_user(self.client)
        self.assertIs(user.is_authenticated, True)
        self.client.post('/user/logout/')
        user = auth.get_user(self.client)
        self.assertIs(user.is_authenticated, False)
