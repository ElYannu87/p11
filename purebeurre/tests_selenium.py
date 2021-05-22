# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from users.models import User
# import time


# class TestSelenium(StaticLiveServerTestCase):
#     def test_no_logs(self):
#         self.browser  = webdriver.Chrome()
#         self.browser.get('http://127.0.0.1:8000/')
#         page = self.browser.find_element_by_id('title')
#         self.assertEqual(page.text, "DU GRAS, OUI, MAIS DE QUALITÉ !")
#         time.sleep(2)
#         search = self.browser.find_element_by_id('term')
#         search.send_keys('test')
#         search.send_keys(Keys.RETURN)
