import pytest

@pytest.mark.django_db
class TestClass():
	def test_front_page(self, client):
		response = client.get('/', follow=True)
		assert b'<title>Memex Explorer</title>' in response.content

	def test_project_page(self, client):
		response = client.get('/add_project', follow=True)
		assert 'base/add_project.html' in response.template_name
		assert b'<form action="" method="post">' in response.content

	def test_add_project(self, client):
		response = client.post('/add_project',
			{'name': 'CATS!', 
			 'description': 'cats cats cats',
			 'icon': 'fa-arrows'},
			follow=True)
		assert 'CATS!' in response.content

