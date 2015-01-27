# Test
from memex.test_utils.unit_test_utils import UnitTestSkeleton
from django.test import TestCase

# App
from crawl_space.forms import AddCrawlForm
from crawl_space.models import Crawl
from base.models import Project


class TestViews(UnitTestSkeleton):

    @classmethod
    def setUpClass(cls):
        super(TestViews, cls).setUpClass()
        test_project = Project(
            name = "Test",
            description = "Description",
            icon = "fa-arrows")
        test_project.save()


    def test_add_crawl_page(self):
        response = self.get('base:crawl_space:add_crawl',
            slugs=dict(slug="test"))
        assert 'crawl_space/add_crawl.html' in response.template_name


# class TestForms(TestCase):
#     pass

    # def test_project_form(self):
    #     form_data = {
    #         'name': 'CATS!',
    #         'description': 'cats cats cats',
    #         'icon': 'fa-arrows'}
    #     form = AddProjectForm(data=form_data)
    #     assert form.is_valid()

