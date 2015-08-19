from __future__ import unicode_literals

import os
import pytest
import requests
import json

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.db import IntegrityError

from rest_framework.test import APITestCase
from rest_framework import status

from base.models import Project


class TestProjectREST(APITestCase):
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
        cls.url = "/api/projects/"

    def parse_response(self, response):
        return json.loads(response.content)[0]

    def test_add_project(self):
        response = self.client.post(self.url, {"name":"Postresttest"}, format="json")
        assert json.loads(response.content)["slug"] == "postresttest"
        assert json.loads(response.content)["name"] == "Postresttest"

    def test_add_project_no_name(self):
        response = self.client.post(self.url, {}, format="json")
        assert json.loads(response.content)["name"][0] == "This field is required."

    def test_add_project_no_name(self):
        response = self.client.post(self.url, {"name":"postrest!"}, format="json")
        assert json.loads(response.content)["name"][0] == "Only numbers, letters, underscores, dashes and spaces are allowed."

    def test_get_all_projects(self):
        response = self.client.get(self.url)
        assert self.parse_response(response)

    def test_get_project_by_id(self):
        response = self.client.get(self.url + "?id=%s" % self.test_project.id)
        assert self.parse_response(response)["id"] == self.test_project.id

    def test_get_project_by_name(self):
        response = self.client.get(self.url + "?name=%s" % self.test_project.name)
        assert self.parse_response(response)["name"] == self.test_project.name

    def test_get_project_by_slug(self):
        response = self.client.get(self.url + "?slug=%s" % self.test_project.slug)
        assert self.parse_response(response)["slug"] == self.test_project.slug

    def test_no_project_exists(self):
        response = self.client.get(self.url + "?id=115")
        assert not response.data

    def test_change_name(self):
        response = self.client.patch(self.url + "%d/" % self.test_project.id,
            {'name':'newname'}, format="json")
        assert json.loads(response.content)["name"] == "newname"

    def test_change_description(self):
        response = self.client.patch(self.url + "%d/" % self.test_project.id,
            {'description':'New Description'}, format="json")
        assert json.loads(response.content)["description"] == "New Description"

    def test_change_slug_fails(self):
        """
        Slug is read-only and cannot be changed. Assert the slug is unchanged.
        """
        response = self.client.patch(self.url + "%d/" % self.test_project.id,
            {'slug':'Bad Slug'}, format="json")
        assert json.loads(response.content)["slug"] == "resttest"
