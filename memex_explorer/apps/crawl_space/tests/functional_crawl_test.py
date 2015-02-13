import pytest
import tempfile

from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import Select

from base.models import Project



@pytest.mark.slow
class TestCrawls(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.browser = WebDriver()
        cls.browser.implicitly_wait(1)
        cls.project = Project.objects.create(
            name="Potatoes",
            description="Why are they?")
        super().setUpClass()


    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()


    @pytest.mark.run(order=1)
    def test_add_crawl_model(self):

        # Names are super awesome
        ff = self.browser

        # Navigate to the project page
        ff.get(self.live_server_url + self.project.get_absolute_url())
        assert "/projects/potatoes" in ff.current_url

        #TODO Use selenium to locate the icon to click via element ID.
        # Click on "Add Crawl Model"
        # add_crawl = ff.find_element_by_...
        ff.get(self.live_server_url +
               self.project.get_absolute_url() +
               'add_crawl_model')

        assert "/projects/potatoes/add_crawl_model" in ff.current_url

        # Click "Submit" on an empty form.
        submit = ff.find_element_by_id('submit-id-submit')
        submit.click()

        # Verify that errors appear as expected
        name_error = ff.find_element_by_id('error_1_id_name')
        assert name_error.text == "This field is required."
        model_error = ff.find_element_by_id('error_1_id_model')
        assert model_error.text == "This field is required."
        features_error = ff.find_element_by_id('error_1_id_features')
        assert features_error.text == "This field is required."

        # Fill out the form with valid input, and submit
        name = ff.find_element_by_id("id_name")
        name.send_keys("Test Crawl Model")

        #TODO locate test model and features file
        # model = ff.find_element_by_id("id_model")
        # with tempfile.NamedTemporaryFile() as f:
        #     f.write(b"")
        #     f.flush()
        #     model.send_keys(f.name)

        #     submit = ff.find_element_by_id('submit-id-submit')
        #     submit.click()

        assert False


    @pytest.mark.run(order=2)
    def test_add_ache_crawl(self):

        ff = self.browser

        # Navigate to the project page
        ff.get(self.live_server_url + self.project.get_absolute_url())
        assert "/projects/potatoes" in ff.current_url

        # # Click on "+ Add Crawl" in the sidebar
        add_crawl = ff.find_element_by_link_text("+ Add Crawl")
        add_crawl.click()
        assert "/projects/potatoes/add_crawl" in ff.current_url

        name = ff.find_element_by_id("id_name")
        name.send_keys("Test ACHE Crawl")

        description = ff.find_element_by_id("id_description")
        description.send_keys("Test description")

        ache_radio = ff.find_element_by_id("id_crawler_2")
        assert ache_radio.get_attribute("value") == "ache"
        ache_radio.click()

        seeds_list = ff.find_element_by_id("id_seeds_list")
        with tempfile.NamedTemporaryFile() as f:
            f.write(b"https://binstar.org/\nhttp://www.continuum.io/")
            f.flush()
            seeds_list.send_keys(f.name)

            submit = ff.find_element_by_id('submit-id-submit')
            submit.click()

        assert "projects/potatoes/crawls/test-ache-crawl/" in ff.current_url


    @pytest.mark.run(order=3)
    def test_add_nutch_crawl(self):

        # Names are awesome
        ff = self.browser

        # Navigate to the project page
        ff.get(self.live_server_url + self.project.get_absolute_url())
        assert "/projects/potatoes" in ff.current_url

        # # Click on "+ Add Crawl" in the sidebar
        add_crawl = ff.find_element_by_link_text("+ Add Crawl")
        add_crawl.click()
        assert "/projects/potatoes/add_crawl" in ff.current_url

        # Click "Submit" on an empty form.
        submit = ff.find_element_by_id('submit-id-submit')
        submit.click()

        # Verify that errors appear as expected
        name_error = ff.find_element_by_id('error_1_id_name')
        assert name_error.text == "This field is required."
        description_error = ff.find_element_by_id('error_1_id_description')
        assert description_error.text == "This field is required."
        seeds_error = ff.find_element_by_id('error_1_id_seeds_list')
        assert seeds_error.text == "This field is required."

        # Fill out the form with valid input, and submit
        name = ff.find_element_by_id("id_name")
        name.send_keys("Test Nutch Crawl")

        description = ff.find_element_by_id("id_description")
        description.send_keys("Test description")

        nutch_radio = ff.find_element_by_id("id_crawler_1")
        assert nutch_radio.get_attribute("value") == "nutch"
        nutch_radio.click()

        seeds_list = ff.find_element_by_id("id_seeds_list")
        with tempfile.NamedTemporaryFile() as f:
            f.write(b"https://binstar.org/\nhttp://www.continuum.io/")
            f.flush()
            seeds_list.send_keys(f.name)

            submit = ff.find_element_by_id('submit-id-submit')
            submit.click()

        assert "projects/potatoes/crawls/test-nutch-crawl/" in ff.current_url
