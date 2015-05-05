from __future__ import unicode_literals

from django.conf import settings
from memex.test_utils.unit_test_utils import UnitTestSkeleton, form_errors, get_object
from django.test import TestCase
from django.db import IntegrityError

from base.models import Project, Index


class TestIndex(UnitTestSkeleton):

    @classmethod
    def setUpClass(cls):
        super(TestIndex, cls).setUpClass()

        cls.test_project = Project(
            name = "Test Indices",
            description = "Test Project Description")
        cls.test_project.save()

