from __future__ import unicode_literals

# Test
from memex.test_utils.unit_test_utils import UnitTestSkeleton, form_errors, get_object
from django.test import TestCase
from django.db import IntegrityError

# App
from base.forms import AddProjectForm
from base.models import Project



class TestViews(UnitTestSkeleton):

    @classmethod
    def setUpClass(cls):
        super(TestViews, cls).setUpClass()

        cls.test_project = Project(
            name = "Project Test",
            description = "Test Project Description")
        cls.test_project.save()

    def test_front_page(self):
        response = self.get('base:index')
        assert 'base/index.html' in response.template_name


    def test_about_page(self):
        response = self.get('base:about')
        assert 'base/about.html' in response.template_name


    def test_add_project_page(self):
        response = self.get('base:add_project')
        assert 'base/add_project.html' in response.template_name


    def test_add_project_no_name(self):
        response = self.post('base:add_project',
            {'description': 'cats cats cats'})
        assert 'This field is required.' in form_errors(response)['name']


    def test_add_project_no_description(self):
        response = self.post('base:add_project',
            {'name': 'CATS'})
        assert 'This field is required.' in form_errors(response)['description']


    def test_add_project_success(self):
        response = self.post('base:add_project',
            {'name': 'CATS',
             'description': 'cats cats cats'})
        assert 'base/project.html' in response.template_name
        assert b'CATS' in response.content


    def test_add_project_with_right_slug(self):
        response = self.get('base:project',
            slugs={'slug': self.test_project.slug})
        assert 'base/project.html' in response.template_name

    def test_project_settings_page(self):
        response = self.get('base:project_settings', 
            slugs={'slug': self.test_project.slug})
        assert 'base/project_update_form.html' in response.template_name

    def test_project_settings_change_name(self):
        response = self.post('base:project_settings',
                {'name': 'Cat Project'}, slugs={'slug': self.test_project.slug}, )
        project = get_object(response)
        assert project.name == 'Cat Project'

    def test_project_settings_change_description(self):
        response = self.post('base:project_settings',
                {'description': 'A project for cats!'}, slugs={'slug': self.test_project.slug}, )
        project = get_object(response)
        assert project.description == 'A project for cats!'


class TestForms(TestCase):

    def setUp(self):
        self.project = Project.objects.create(name="Bicycles for sale", description="Project about bicycles")

    def test_project_form(self):
        form_data = {
            'name': 'CATS',
            'description': 'cats cats cats'}
        form = AddProjectForm(data=form_data)
        assert form.is_valid()

    def test_project_form_no_name(self):
        form_data = {
            'description': 'cats cats cats'}
        form = AddProjectForm(data=form_data)
        assert form.is_valid() is False
        assert 'This field is required.' in form.errors['name']

    def test_project_form_no_description(self):
        form_data = {
            'name': 'CATS'}
        form = AddProjectForm(data=form_data)
        assert form.is_valid() is False
        assert 'This field is required.' in form.errors['description']

    def test_existing_project_error(self):
        form_data = {
            'name': 'Bicycles for sale',
            'description': 'cats cats cats'}
        form = AddProjectForm(data=form_data)
        assert form.is_valid() is False
        assert 'Project with this Name already exists.' in form.errors['name']


class TestProjectQueries(TestCase):

    def setUp(self):
        project = Project.objects.create(name=u"Bicycles for sale", description="Project about bicycles")
        self.project = project

    def test_project_exists(self):
        assert Project.objects.get(name="Bicycles for sale")

    def test_unique_project(self):
        with self.assertRaises(IntegrityError):
            Project.objects.create(name="Bicycles for sale", description="Project about bicycles")

    def test_get_by_slug(self):
        assert 'bicycles-for-sale' == self.project.slug

