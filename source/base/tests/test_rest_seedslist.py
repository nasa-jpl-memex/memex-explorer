import json

from rest_framework.test import APITestCase
from rest_framework import status

from base.models import SeedsList

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.db import IntegrityError


class TestSeedsListREST(APITestCase):
    """
    Testing for adding Projects through the REST framework.
    """
    @classmethod
    def setUpClass(cls):
        cls.test_seeds = SeedsList(
            name="RestSeeds",
            seeds="""
            http://www.reddit.com/r/aww
            http://gizmodo.com/of-course-japan-has-an-island-where-cats-outnumber-peop-1695365964
            http://en.wikipedia.org/wiki/Cat
            http://www.catchannel.com/
            http://mashable.com/category/cats/
            http://www.huffingtonpost.com/news/cats/
            http://www.lolcats.com/
            """
        )
        cls.test_seeds.save()
        cls.url = "/api/seeds_list/"

    def test_get_seeds_list(self):
        response = self.client.get(self.url, {"name": "RestSeeds"}, format="json")
        assert json.loads(response.content)[0]["name"] == "RestSeeds"
