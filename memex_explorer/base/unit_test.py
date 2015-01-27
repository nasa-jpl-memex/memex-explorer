# Test
from django.test import TestCase, Client

# App
from base.forms import AddProjectForm

# Utility
from django.core.urlresolvers import reverse

def form_errors(response):
    return response.context['form'].errors

class TestViews(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = Client()


    @classmethod
    def get(cls, view_name, *args, **kwargs):
        if 'slugs' in kwargs:
            slugs = kwargs.pop('slugs')
            return cls.client.get(
                reverse(view_name, kwargs=slugs),
                *args, follow=True, **kwargs)
        else:
            return cls.client.get(reverse(view_name),
                *args, follow=True, **kwargs)

    @classmethod
    def post(cls, view_name, *args, **kwargs):
        if 'slugs' in kwargs:
            slugs = kwargs.pop('slugs')
            return cls.client.post(
                reverse(view_name, kwargs=slugs),
                *args, follow=True, **kwargs)
        else:
            return cls.client.post(reverse(view_name),
                *args, follow=True, **kwargs)


    def test_front_page(self):
        response = self.get('base:index')
        assert 'base/index.html' in response.template_name


    def test_project_page(self):
        response = self.post('base:add_project')
        assert 'base/add_project.html' in response.template_name


    def test_add_project_no_name(self):
        response = self.post('base:add_project',
            {'description': 'cats cats cats',
             'icon': 'fa-arrows'})
        assert 'This field is required.' in form_errors(response)['name']


    def test_add_project_no_description(self):
        response = self.post('base:add_project',
            {'name': 'CATS!',
             'icon': 'fa-arrows'})
        assert 'This field is required.' in form_errors(response)['description']


    def test_add_project(self):
        response = self.post('base:add_project',
            {'name': 'CATS!',
             'description': 'cats cats cats',
             'icon': 'fa-arrows'})
        assert 'base/index.html' in response.template_name
        assert b'CATS!' in response.content


    def test_add_project_with_slug(self):
        self.test_add_project()

        response = self.get('base:project',
            slugs=dict(slug="cats"))
        assert 'base/project.html' in response.template_name


class TestForms(TestCase):

    def test_project_form(self):
        form_data = {
            'name': 'CATS!',
            'description': 'cats cats cats',
            'icon': 'fa-arrows'}
        form = AddProjectForm(data=form_data)
        assert form.is_valid()


    def test_project_form_no_name(self):
        form_data = {
            'description': 'cats cats cats',
            'icon': 'fa-arrows'}
        form = AddProjectForm(data=form_data)
        assert form.is_valid() is False
