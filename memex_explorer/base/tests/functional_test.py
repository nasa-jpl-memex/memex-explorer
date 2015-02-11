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

        # Names are awesome
        ff = self.browser

        ff.get(self.live_server_url)
        assert ff.title == 'Memex Explorer'

        # Click on "New Project".
        new_project = ff.find_element_by_link_text("New Project")
        new_project.click()

        # Click "Submit" on an empty form.
        submit = ff.find_element_by_id('submit-id-submit')
        submit.click()

        # Verify that errors appear as expected
        name_error = ff.find_element_by_id("error_1_id_name")
        assert name_error.text == 'This field is required.' 
        description_error = ff.find_element_by_id("error_1_id_description")
        assert description_error.text == 'This field is required.' 

        # Fill out the form and submit
        name = ff.find_element_by_id("id_name")
        name.send_keys("Test name")
        description = ff.find_element_by_id("id_description")
        description.send_keys("Test description")
        submit = ff.find_element_by_id('submit-id-submit')
        submit.click()

        # Verify that we are redirected to the project page
        assert ff.current_url == self.live_server_url + '/projects/test-name/'


