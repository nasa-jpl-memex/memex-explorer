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

    def test_add_project(self):
        response = self.client.post("/api/projects/", {"name":"potatoresttest"}, format="json")
        assert response.data["slug"] == "potatoresttest"

    def test_get_all_projects(self):
        response = self.client.get("/api/projects/")
        assert response.data

    def test_get_project_by_id(self):
        response = self.client.get("/api/projects/?id=1", format="json")
