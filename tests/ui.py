__author__ = 'knichols'
import re
import time
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys

# Selenium Tests
class BaseTestCase(LiveServerTestCase):

    fixtures = ['alertdb_people_auth']

    @classmethod
    def setUpClass(cls):
        cls.driver = WebDriver()
        super(BaseTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(BaseTestCase, cls).tearDownClass()
        cls.driver.quit()


class AuthTests(BaseTestCase):

    def test(self):
        self.driver.get(self.live_server_url)

    def test_register(self):
        self.driver.get(self.live_server_url + '/accounts/signup/')
        src = self.driver.page_source
        print src
        username = self.driver.find_element_by_id('id_email')
        username.send_keys('test@alerted.us')

        password1 = self.driver.find_element_by_id('id_password1')
        password1.send_keys('password')
        password2 = self.driver.find_element_by_id('id_password2')
        password2.send_keys('password')
        password2.submit()
        time.sleep(2)
        src = self.driver.page_source
        text_found = re.search(r'Saved Locations', src)
        self.assertTrue(text_found)
        self.driver.get(self.live_server_url + '/accounts/logout/')

    def test_login(self):
        self.driver.get(self.live_server_url + '/accounts/login/')
        username = self.driver.find_element_by_id('id_login')
        username.send_keys('admin@alerted.us')
        password = self.driver.find_element_by_id('id_password')
        password.send_keys('password')
        password.submit()
        time.sleep(2)
        src = self.driver.page_source
        text_found = re.search(r'Saved Locations', src)
        self.assertTrue(text_found)
        autocomplete = self.driver.find_element_by_id('Autocomplete')
        autocomplete.send_keys("1600 pennsyl")
        autocomplete.send_keys(Keys.ARROW_DOWN )
        autocomplete.click()
        autocomplete.submit()
        # TODO test for Angular rows

        self.driver.get(self.live_server_url + '/accounts/logout/')