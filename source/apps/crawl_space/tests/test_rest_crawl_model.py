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

from apps.crawl_space.models import CrawlModel, Crawl
from base.models import Project


class TestCrawlModelREST(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_project = Project(
            name="Test Crawl Model Project REST",
        )
        cls.test_project.save()

        cls.test_crawlmodel = CrawlModel(
            name="Test Crawl Model REST",
            model = cls.get_model_file(),
            features = cls.get_features_file(),
            project = cls.test_project
        )
        cls.test_crawlmodel.save()
        cls.url = "/api/crawl_models/"

    @classmethod
    def testDownClass(cls):
        super(TestCrawlModelREST, cls).tearDownClass()
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

    def test_crawl_models_endpoint(self):
        response = self.client.get(self.url)
        assert self.parse_response(response)

    def test_get_crawlmodel_by_id(self):
        response = self.client.get(self.url + "?id=%s" % self.test_crawlmodel.id)
        assert self.parse_response(response)["id"] == self.test_crawlmodel.id

    def test_get_crawlmodel_by_name(self):
        response = self.client.get(self.url + "?name=%s" % self.test_crawlmodel.name)
        assert self.parse_response(response)["name"] == self.test_crawlmodel.name

    def test_get_crawlmodel_by_slug(self):
        response = self.client.get(self.url + "?slug=%s" % self.test_crawlmodel.slug)
        assert self.parse_response(response)["slug"] == self.test_crawlmodel.slug

    def test_get_crawlmodel_by_project(self):
        response = self.client.get(self.url + "?project=%s" % self.test_crawlmodel.project.id)
        assert self.parse_response(response)["project"] == self.test_crawlmodel.project.id

    def test_add_crawl_model_rest(self):
        data = {"name": "Crawl Model POST REST", "features": self.get_features_file(),
            "model": self.get_model_file(), "project": self.test_project.id}
        response = self.client.post(self.url, data, format="multipart")
        assert json.loads(response.content)["name"] == "Crawl Model POST REST"

    def test_add_crawl_model_bad_festures(self):
        data = {"name": "Crawl Model POST REST", "features": self.get_model_file(),
            "model": self.get_model_file(), "project": self.test_project.id}
        response = self.client.post(self.url, data, format="multipart")
        assert json.loads(response.content)["features"]

    def test_add_crawl_model_bad_model(self):
        data = {"name": "Crawl Model POST REST", "features": self.get_features_file(),
            "model": self.get_features_file(), "project": self.test_project.id}
        response = self.client.post(self.url, data, format="multipart")
        assert json.loads(response.content)["model"]

    def test_change_slug_fails(self):
        """
        Slug is read-only and cannot be changed. Assert the slug is unchanged.
        """
        response = self.client.patch(self.url + "%d/" % self.test_crawlmodel.id,
            {'slug':'Bad Slug'}, format="json")
        assert json.loads(response.content)["slug"] == "test-crawl-model-rest"

    def test_add_crawl_model_no_project(self):
        data = {"name": "Crawl Model POST REST", "features": self.get_features_file(),
            "model": self.get_model_file()}
        response = self.client.post(self.url, data, format="multipart")
        assert json.loads(response.content)["project"][0]

    def test_add_crawl_model_no_name(self):
        data = {"features": self.get_features_file(),
            "model": self.get_model_file(), "project": self.test_project.id}
        response = self.client.post(self.url, data, format="multipart")
        assert json.loads(response.content)["name"][0]

    def test_add_crawl_model_no_model(self):
        data = {"name": "Crawl Model POST REST", "features": self.get_features_file(),
            "project": self.test_project.id}
        response = self.client.post(self.url, data, format="multipart")
        assert json.loads(response.content)["model"]

    def test_add_crawl_model_no_features(self):
        data = {"name": "Crawl Model POST REST", "model": self.get_model_file(),
            "project": self.test_project.id}
        response = self.client.post(self.url, data, format="multipart")
        assert json.loads(response.content)["features"]

    def test_add_crawl_model_no_features(self):
        data = {"name": "Crawl Model POST REST", "model": self.get_model_file(),
            "project": self.test_project.id}
        response = self.client.post(self.url, data, format="multipart")

    def test_delete_crawl_model(self):
        data = {"name": "Crawl Model POST REST", "features": self.get_features_file(),
            "model": self.get_model_file(), "project": self.test_project.id}
        model = json.loads(self.client.post(self.url, data, format="multipart").content)
        response = self.client.delete(self.url + str(model["id"]) + "/", format="multipart")
        assert not response.content

    def test_delete_crawl_integrity_error(self):
        data = {"name": "Crawl Model POST REST", "features": self.get_features_file(),
            "model": self.get_model_file(), "project": self.test_project.id}
        model = json.loads(self.client.post(self.url, data, format="multipart").content)
        data = {"name": "Ache POST REST", "crawler": "ache", "seeds_list": self.get_seeds(),
            "project": self.test_project.id, "crawl_model": model["id"]}
        crawl = json.loads(self.client.post("/api/crawls/", data, format="multipart").content)
        error = json.loads(self.client.delete(self.url + str(model["id"]) + "/", format="multipart").content)
        assert error["errors"][0] == crawl["name"]
