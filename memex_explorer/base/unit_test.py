import pytest

@pytest.mark.django_db
class TestClass():
	def test_right_page(self, client):
		response = client.get('/base', follow=True)
		assert b"MEMEX" in response.content

	def test_add_project(self, client):
		response = client.post('/base/add_project',
			{'name': 'CATS!', 
			 'description': 'cats cats cats',
			 'icon': 'fa-arrows'},
			follow=True)
		assert False

