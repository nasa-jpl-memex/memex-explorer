import json

from rest_framework.test import APITestCase
from rest_framework import status

from base.models import SeedsList

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.db import IntegrityError
from django.core.files.uploadedfile import SimpleUploadedFile


class TestSeedsListREST(APITestCase):
    """
    Testing for adding Projects through the REST framework.
    """
    @classmethod
    def setUpClass(cls):
        cls.seeds=[
            "http://www.reddit.com/r/aww",
            "http://gizmodo.com/of-course-japan-has-an-island-where-cats-outnumber-peop-1695365964",
            "http://en.wikipedia.org/wiki/Cat",
            "http://www.catchannel.com/",
            "http://mashable.com/category/cats/",
            "http://www.huffingtonpost.com/news/cats/",
            "http://www.lolcats.com/"
        ]
        cls.seeds_string = """http://www.reddit.com/r/aww
            http://gizmodo.com/of-course-japan-has-an-island-where-cats-outnumber-peop-1695365964
            http://en.wikipedia.org/wiki/Cat
            http://www.catchannel.com/
            http://mashable.com/category/cats/
            http://www.huffingtonpost.com/news/cats/
            http://www.lolcats.com/"""
        cls.seeds_file = SimpleUploadedFile('ht.seeds', bytes("http://www.google.com"), 'utf-8')
        cls.test_seeds = SeedsList(
            name="RestSeeds",
            seeds = json.dumps(cls.seeds),
        )
        cls.test_seeds.save()
        cls.url = "/api/seeds_list/"

    def test_get_all_seeds(self):
        response = self.client.get(self.url, format="json")
        assert json.loads(response.content)[0]["seeds"] == self.test_seeds.seeds

    def test_get_seeds_by_id(self):
        response = self.client.get(self.url + "?id=%s" % self.test_seeds.id)
        assert json.loads(response.content)[0]["id"] == self.test_seeds.id

    def test_get_seeds_by_slug(self):
        response = self.client.get(self.url + "?slug=%s" % self.test_seeds.slug)
        assert json.loads(response.content)[0]["slug"] == self.test_seeds.slug

    def test_get_seeds_by_name(self):
        response = self.client.get(self.url + "?name=%s" % self.test_seeds.name)
        assert json.loads(response.content)[0]["name"] == self.test_seeds.name

    def test_add_seeds_post(self):
        response = self.client.post(self.url, {"name": "test_seeds_post",
            "seeds": json.dumps(self.seeds)}, format="json")
        assert json.loads(response.content)["name"] == "test_seeds_post"

    def test_add_seeds_file(self):
        response = self.client.post(self.url, {"name": "test_seeds_post1",
            "seeds": self.seeds_file}, format="multipart")
        assert json.loads(response.content)["name"] == "test_seeds_post1"

    def test_add_seeds_string(self):
        response = self.client.post(self.url, {"name": "test_seeds_post2",
            "textseeds": self.seeds_string}, format="json")
        assert json.loads(response.content)["name"] == "test_seeds_post2"

    def test_add_seeds_no_name(self):
        response = self.client.post(self.url, {"seeds": self.seeds}, format="json")
        assert json.loads(response.content)["name"][0] == "This field is required."

    def test_add_seeds_no_seeds(self):
        response = self.client.post(self.url, {"name": "test_seeds_post"}, format="json")
        assert json.loads(response.content)["seeds"][0] == "This field is required."

    def test_change_name(self):
        response = self.client.patch(self.url + "%d/" % self.test_seeds.id,
            {"name": "cats_seeds"}, format="json")
        assert json.loads(response.content)["name"] == "cats_seeds"

    def test_change_seeds(self):
        response = self.client.patch(self.url + "%d/" % self.test_seeds.id,
            {"seeds": json.dumps(["http://www.lolcats.com/", "http://www.reddit.com/r/me_irl/"])}, format="json")
        assert json.loads(json.loads(response.content)["seeds"]) == ["http://www.lolcats.com/", "http://www.reddit.com/r/me_irl/"]

    def test_non_json(self):
        response = self.client.patch(self.url + "%d/" % self.test_seeds.id,
            {"seeds": ["http://www.lolcats.com/", "http://www.reddit.com/r/me_irl/"]}, format="json")
        assert json.loads(response.content)["seeds"][0] == "Seeds must be a JSON encoded string."

    def test_not_array(self):
        response = self.client.patch(self.url + "%d/" % self.test_seeds.id,
            {"seeds": json.dumps("http://www.lolcats.com/\nhttp://www.reddit.com/r/me_irl/")}, format="json")
        assert json.loads(response.content)["seeds"][0] == "Seeds must be an array of URLs."

    def test_not_url(self):
        response = self.client.patch(self.url + "%d/" % self.test_seeds.id,
            {"seeds": json.dumps(["a", "b"])}, format="json")
        assert json.loads(response.content)["seeds"] == ["The seeds list contains invalid urls.", {'0': "a"}, {'1': "b"}, {'list': 'a\nb'}]
