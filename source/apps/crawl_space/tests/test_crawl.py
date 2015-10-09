from __future__ import unicode_literals

import os
import shutil
import json

# Test
from memex.test_utils.unit_test_utils import UnitTestSkeleton, form_errors, get_object
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

import pytest

# App
from apps.crawl_space.forms import AddCrawlForm
from apps.crawl_space.models import Crawl, CrawlModel
from base.models import Project, SeedsList, alphanumeric_validator


def assert_form_errors(response, *errors):
    """Given a response, assert that only the given `errors`
    are present in the form response."""

    efe = expected_form_errors = set(errors)
    assert set(form_errors(response).keys()) - efe == set()


class TestViews(UnitTestSkeleton):

    @classmethod
    def setUpClass(cls):
        """Initialize a test project and crawl model,
        and save them to the test database."""
        super(TestViews, cls).setUpClass()

        cls.test_project = Project(
            name = "Test",
            description = "Test Project Description"
        )
        cls.test_project.save()

        cls.test_seeds_list = SeedsList(
            name = "Test Seeds",
            seeds = json.dumps([
                "http://www.reddit.com/r/aww",
                "http://gizmodo.com/of-course-japan-has-an-island-where-cats-outnumber-peop-1695365964",
                "http://en.wikipedia.org/wiki/Cat",
                "http://www.catchannel.com/",
                "http://mashable.com/category/cats/",
                "http://www.huffingtonpost.com/news/cats/",
                "http://www.lolcats.com/"
            ]),
        )
        cls.test_seeds_list.save()

        cls.test_crawl = Crawl(
            name = "Test Crawl",
            description = "Test Crawl Description",
            crawler = "nutch",
            config = "config_default",
            project = cls.test_project,
            seeds_object = cls.test_seeds_list
        )
        cls.test_crawl.save()

    @classmethod
    def get_seeds(self):
        """Return a new instance of SimpleUploadedFile. This file can only
        be used once."""

        return SimpleUploadedFile('ht.seeds', bytes('This is some content.\n'), 'utf-8')

    @property
    def crawl_slugs(self):
        """Return a dictionary with a "test" project slug and
        a "test-crawl" crawl slug."""

        return dict(slugs=dict(
            project_slug="test",
            crawl_slug="test-crawl"))

    def test_crawl_delete(self):
        response = self.post('base:crawl_space:delete_crawl',
            **self.crawl_slugs)
        assert 'base/project.html' in response.template_name
