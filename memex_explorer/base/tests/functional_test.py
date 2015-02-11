import unittest
import pytest

from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

@pytest.mark.slow
class TestProject(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.browser = WebDriver()
        cls.browser.implicitly_wait(1)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def test_add_project(self):
        self.browser.get(self.live_server_url)
        assert self.browser.title == 'Memex Explorer'

        # Click on "New Project".
        new_project = self.browser.find_element_by_link_text("New Project")
        new_project.click()

        # Click "Submit" on an empty form.
        submit = self.browser.find_element_by_id('submit-id-submit')
        submit.click()


        name_error = bb.find_element_by_id("error_1_id_name")
        assert name_error == 'This field is required.' 
        description_error = bb.find_element_by_id("error_1_id_description")
        assert description_error == 'This field is required.' 

        assert False

