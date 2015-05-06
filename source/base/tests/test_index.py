from __future__ import unicode_literals

import os

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
            name="Test Indices",
            description="Test Project Description"
        )
        cls.test_project.save()

        cls.test_index = Index(
            name="Test Index",
            project=cls.test_project,
            uploaded_data=os.path.join(settings.MEDIA_ROOT, "sample.zip")
        )
        cls.test_index.save()
        import ipdb
        ipdb.set_trace()

    def test_assert_one(self):
        assert 1

