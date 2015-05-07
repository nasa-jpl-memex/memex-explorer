from __future__ import unicode_literals

import os
import shutil

from django.conf import settings
from memex.test_utils.unit_test_utils import UnitTestSkeleton, form_errors, get_object
from django.test import TestCase
from django.db import IntegrityError
from django.core.files.uploadedfile import UploadedFile
from django.core.files import File
from django.utils.text import slugify

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

    @classmethod
    def tearDownClass(cls):
        super(TestIndex, cls).tearDownClass()
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, "indices", "test-index"))

    @classmethod
    def zip_file(self):
        return File(open(os.path.join(settings.MEDIA_ROOT, "sample.zip"), 'r'))

    def slugs(self):
        """Return a dictionary with a "test" project slug."""
        return dict(slugs=dict(
            project_slug="test-indices"))

    def get_form_data(self):
        return {
            "name": "Test Index",
            "project": self.test_project,
            "uploaded_data": self.zip_file(),
        }

    def test_add_index(self):
        response = self.post('base:add_index', self.get_form_data(), **self.slugs())
        assert 'base/index_update_form.html' in response.template_name

