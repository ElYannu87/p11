from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client

# Create your tests here.


class PagesViewTest(TestCase):
    """
    This class contains tests about views of application 'pages'
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

    def test_home_view_has_status_code_200(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_home_view_content_is_home_template(self):
        response = self.client.get('')
        self.assertContains(response, "Du gras, oui, Mais de Qualité !")
