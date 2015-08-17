from __future__ import unicode_literals

import os
import pytest
import requests

from django.conf import settings

from memex.test_utils.unit_test_utils import UnitTestSkeleton, get_object
from django.test import TestCase
from django.db import IntegrityError


from base.models import Project


class TestRestProject(TestCase):
    """
    Testing for adding Projects through the REST framework.
    """
    @classmethod
    def setUpClass(cls):
        cls.url = "http://localhost:8000/api/projects"
        cls.test_project = Project(
            name = "Project Test",
            description = "Test Project Description")
        cls.test_project.save()


    def test_get_all_projects(self):
        response = requests.get(url=self.url)
        assert response.status_code == 200
