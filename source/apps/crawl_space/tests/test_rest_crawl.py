from __future__ import unicode_literals

import os
import pytest
import requests
import json
import shutil

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
    def tearDownClass(cls):
        super(TestCrawlREST, cls).tearDownClass()
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, "crawls"))
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, "models"))

    @classmethod
    def get_model_file(self):
        return SimpleUploadedFile('pageclassifier.model', bytes('This is a model file.\n'), 'utf-8')

    @classmethod
    def get_features_file(self):
        return SimpleUploadedFile('pageclassifier.features', bytes('This is a features file.\n'), 'utf-8')

    @classmethod
    def get_seeds(self):
        return SimpleUploadedFile('ht.seeds', bytes('This is some content.\n'))

    def parse_response(self, response):
        return json.loads(response.content)[0]

    def test_crawls_endpoint(self):
        response = self.client.get(self.url)
        assert self.parse_response(response)

    def test_get_crawl_by_name(self):
        response = self.client.get(self.url + "?name=%s" % self.test_nutch_crawl.name)
        assert self.parse_response(response)["name"] == "Test Nutch REST"

    def test_get_crawl_by_slug(self):
        response = self.client.get(self.url + "?slug=%s" % self.test_nutch_crawl.slug)
        assert self.parse_response(response)["slug"] == "test-nutch-rest"

    def test_get_crawl_by_description(self):
        response = self.client.get(self.url + "?description=%s" % self.test_nutch_crawl.description)
        assert self.parse_response(response)["description"] == "Test Crawl Description"

    def test_get_crawl_by_status(self):
        response = self.client.get(self.url + "?status=%s" % self.test_nutch_crawl.status)
        assert self.parse_response(response)["status"] == "NOT STARTED"

    def test_get_crawl_by_project(self):
        response = self.client.get(self.url + "?project=%d" % self.test_nutch_crawl.project.id)
        assert self.parse_response(response)["project"] == self.test_project.id

    def test_get_crawl_by_crawl_model(self):
        response = self.client.get(self.url + "?crawl_model=%d" % self.test_ache_crawl.crawl_model.id)
        assert self.parse_response(response)["crawl_model"] == self.test_crawlmodel.id

    def test_get_crawl_by_crawler(self):
        response = self.client.get(self.url + "?crawler=%s" % self.test_nutch_crawl.crawler)
        assert self.parse_response(response)["crawler"] == self.test_nutch_crawl.crawler

    def test_add_crawl_rest_nutch(self):
        data = {"name": "Nutch POST REST", "crawler": "nutch", "seeds_list": self.get_seeds(),
            "project": self.test_project.id}
        response = self.client.post(self.url, data, format="multipart")
        assert json.loads(response.content)["name"] == "Nutch POST REST"

    def test_add_crawl_rest_ache(self):
        data = {"name": "Ache POST REST", "crawler": "ache", "seeds_list": self.get_seeds(),
            "project": self.test_project.id, "crawl_model": self.test_crawlmodel.id}
        response = self.client.post(self.url, data, format="multipart")
        assert json.loads(response.content)["name"] == "Ache POST REST"

    def test_add_crawl_textseeds(self):
        """
        Test if the application can create a seeds list from text.
        """
        data = {"name": "Nutch POST Textseeds", "crawler": "nutch", "textseeds": "http://www.google.com",
            "project": self.test_project.id}
        response = self.client.post(self.url, data, format="multipart")
        assert json.loads(response.content)["name"] == "Nutch POST Textseeds"

    def test_crawl_change_name(self):
        response = self.client.patch(self.url + "%d/" % self.test_nutch_crawl.id,
            {'name':'new name'}, format="json")
        assert json.loads(response.content)["name"] == "new name"

    def test_crawl_change_description(self):
        response = self.client.patch(self.url + "%d/" % self.test_nutch_crawl.id,
            {'description':'this is a new description'}, format="json")
        assert json.loads(response.content)["description"] == "this is a new description"

    def test_change_slug_fails(self):
        """
        Slug is read-only and cannot be changed. Assert the slug is unchanged.
        """
        response = self.client.patch(self.url + "%d/" % self.test_nutch_crawl.id,
            {'slug':'Bad Slug'}, format="json")
        assert json.loads(response.content)["slug"] == "test-nutch-rest"

    def test_add_crawl_no_model(self):
        data = {"name": "Ache POST No Model", "crawler": "ache", "textseeds": "http://www.google.com",
            "project": self.test_project.id}
        response = self.client.post(self.url, data, format="multipart")
        assert json.loads(response.content)["crawler"][0] == "Ache crawls require a Crawl Model"
