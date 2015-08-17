from __future__ import unicode_literals

import os
import pytest
import requests
import json

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.db import IntegrityError
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APITestCase
from rest_framework import status

from apps.crawl_space.models import Crawl, CrawlModel
from base.models import Project


class TestCrawlREST(APITestCase):
    """
    Testing for adding Crawls through Django REST Framework
    """
    @classmethod
    def setUpClass(cls):
        cls.test_project = Project(
            name="Test Crawl Project REST",
        )
        cls.test_project.save()

        cls.test_nutch_crawl = Crawl(
            name = "Test Nutch REST",
            description = "Test Crawl Description",
            crawler = "nutch",
            config = "config_default",
            seeds_list = cls.get_seeds(),
            project = cls.test_project
        )
        cls.test_nutch_crawl.save()

        cls.test_crawlmodel = CrawlModel(
            name = "Test Model Crawls REST",
            model = cls.get_model_file(),
            features = cls.get_features_file(),
            project = cls.test_project,
        )
        cls.test_crawlmodel.save()

        cls.test_ache_crawl = Crawl(
            name = "Test Ache REST",
            description = "Test Crawl Description",
            crawler = "ache",
            config = "config_default",
            seeds_list = cls.get_seeds(),
            project = cls.test_project,
            crawl_model = cls.test_crawlmodel
        )
        cls.test_ache_crawl.save()

        cls.url = "/api/crawls/"

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

    def test_crawls_endpoint(self):
        response = self.client.get(self.url)
        assert response

    def test_crawl_query_name(self):
        response = self.client.get(self.url + "?name=%s" % self.test_nutch_crawl.name)
        assert json.loads(response.content)[0]["name"] == "Test Nutch REST"

    def test_crawl_query_slug(self):
        response = self.client.get(self.url + "?slug=%s" % self.test_nutch_crawl.slug)
        assert json.loads(response.content)[0]["slug"] == "test-nutch-rest"

    def test_crawl_query_description(self):
        response = self.client.get(self.url + "?description=%s" % self.test_nutch_crawl.description)
        assert json.loads(response.content)[0]["description"] == "Test Crawl Description"

    def test_crawl_query_status(self):
        response = self.client.get(self.url + "?status=%s" % self.test_nutch_crawl.status)
        assert json.loads(response.content)[0]["status"] == "NOT STARTED"

    def test_crawl_query_project(self):
        response = self.client.get(self.url + "?project=%d" % self.test_nutch_crawl.project.id)
        assert json.loads(response.content)[0]["project"] == self.test_project.id

    def test_crawl_query_crawl_model(self):
        response = self.client.get(self.url + "?crawl_model=%d" % self.test_ache_crawl.crawl_model.id)
        assert json.loads(response.content)[0]["crawl_model"] == self.test_crawlmodel.id

    def test_crawl_query_crawler(self):
        response = self.client.get(self.url + "?crawler=%s" % self.test_nutch_crawl.crawler)
        assert json.loads(response.content)[0]["crawler"] == self.test_nutch_crawl.crawler
