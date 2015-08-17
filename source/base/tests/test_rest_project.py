from __future__ import unicode_literals

import os
import pytest
import requests
import json

from django.conf import settings
from django.core.urlresolvers import reverse

from memex.test_utils.unit_test_utils import UnitTestSkeleton, get_object
from django.test import TestCase
from django.db import IntegrityError

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from base.models import Project


class TestRestProject(APITestCase):
    """
    Testing for adding Projects through the REST framework.
    """
    @classmethod
    def setUpClass(cls):
        cls.test_project = Project(
            name = "RestTest",
            description = "Testing Rest API"
        )
        cls.test_project.save()

    def test_add_project(self):
        response = self.client.post("/api/projects/", {"name":"Postresttest"}, format="json")
        assert response.data["slug"] == "postresttest"
        assert response.data["name"] == "Postresttest"

    def test_add_project_no_name(self):
        response = self.client.post("/api/projects/", {}, format="json")
        assert response.data["name"][0] == "This field is required."

    def test_add_project_no_name(self):
        response = self.client.post("/api/projects/", {"name":"potatorest!"}, format="json")
        assert response.data["name"][0] == "Only numbers, letters, underscores, dashes and spaces are allowed."

    def test_get_all_projects(self):
        response = self.client.get("/api/projects/")
        assert response.data

    def test_get_project_by_id(self):
        response = self.client.get("/api/projects/?id=%s" % self.test_project.id)
        assert response.data

    def test_get_project_by_name(self):
        response = self.client.get("/api/projects/?name=%s" % self.test_project.name)
        assert response.data

    def test_get_project_by_slug(self):
        response = self.client.get("/api/projects/?slug=%s" % self.test_project.slug)
        assert response.data

    def test_no_project_exists(self):
        response = self.client.get("/api/projects/?id=115")
        assert not response.data
