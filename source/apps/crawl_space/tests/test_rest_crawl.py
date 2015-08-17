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

from apps.crawl_space.models import Crawl
from base.models import Project


class TestCrawlREST(APITestCase):
    """
    Testing for adding Crawls through Django REST Framework
    """
    def setUpClass(cls):
        cls.nutch_crawl = Crawl(
            name = "Test Crawl",
            description = "Test Crawl Description",
            crawler = "nutch",
            config = "config_default",
            seeds_list = cls.get_seeds(),
            project = cls.test_project
        )
        cls.test_crawl.save()

        cls.test_crawlmodel = CrawlModel(
            name = "Test Crawl Model",
            model = cls.get_model_file(),
            features = cls.get_features_file(),
            project = cls.test_project,
        )
        cls.test_crawlmodel.save()

    @classmethod
    def get_model_file(self):
        return SimpleUploadedFile('pageclassifier.model', bytes('This is a model file.\n'), 'utf-8')

    @classmethod
    def get_features_file(self):
        return SimpleUploadedFile('pageclassifier.features', bytes('This is a features file.\n'), 'utf-8')

    @classmethod
    def get_seeds(self):
        """Return a new instance of SimpleUploadedFile. This file can only
        be used once."""

        return SimpleUploadedFile('ht.seeds', bytes('This is some content.\n'), 'utf-8')
