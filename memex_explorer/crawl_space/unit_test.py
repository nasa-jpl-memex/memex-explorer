# # Test
# from django.test import TestCase, Client

# # App
# from base.forms import AddProjectForm
# from base.models import Project



# # Utility functions
# def form_errors(response):
#     return response.context['form'].errors

# class TestViews(TestCase):

#     @classmethod
#     def setUpClass(cls):
#         cls.client = Client()


#     def test_project_page(self):
#         response = self.client.get('/test', follow=True)
#         assert 'base/index.html' in response.template_name


# class TestForms(TestCase):
#     pass

#     # def test_project_form(self):
#     #     form_data = {
#     #         'name': 'CATS!',
#     #         'description': 'cats cats cats',
#     #         'icon': 'fa-arrows'}
#     #     form = AddProjectForm(data=form_data)
#     #     assert form.is_valid()

