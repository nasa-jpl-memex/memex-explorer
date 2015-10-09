from __future__ import unicode_literals

import os
import shutil
import json

# Test
from memex.test_utils.unit_test_utils import UnitTestSkeleton, form_errors, get_object
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

# App
from apps.crawl_space.models import Crawl, CrawlModel
from base.models import Project, SeedsList, alphanumeric_validator

from apps.crawl_space.models import Crawl
from apps.crawl_space.viz.plot import AcheDashboard

from memex.test_settings import TEST_CRAWL_DATA


class TestPlots(UnitTestSkeleton):

    @classmethod
    def setUpClass(cls):
        """Initialize a test project and crawl model,
        and save them to the test database."""

        super(TestPlots, cls).setUpClass()

        cls.test_project = Project(
            name = "Test Project",
            description = "Test Project Description"
        )
        cls.test_project.save()

        cls.test_seeds_list = SeedsList(
            name = "Test Seeds New",
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

        cls.test_crawlmodel = CrawlModel(
            name = "Test Model",
            model = cls.get_model_file(),
            features = cls.get_features_file(),
            project = cls.test_project,
        )
        cls.test_crawlmodel.save()

        cls.test_crawl = Crawl(
            name = "Test Crawl Plots",
            description = "Test Crawl Description",
            crawler = "ache",
            config = "config_default",
            seeds_object = cls.test_seeds_list,
            project = cls.test_project,
            crawl_model = cls.test_crawlmodel,
        )
        cls.test_crawl.save()
        cls.dashboard = AcheDashboard(cls.test_crawl)
        cls.dashboard.domain.crawled_data = os.path.join(TEST_CRAWL_DATA, "crawledpages.csv")
        cls.dashboard.domain.relevant_data = os.path.join(TEST_CRAWL_DATA, "relevantpages.csv")
        cls.dashboard.harvest.harvest_data = os.path.join(TEST_CRAWL_DATA, "harvestinfo.csv")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.test_crawl.get_crawl_path())

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

    def test_domain(self):
        domain = self.dashboard.get_domain_plot()
        for x in domain:
            assert x

    def test_harvest(self):
        harvest = self.dashboard.get_harvest_plot()
        for x in harvest:
            assert x
