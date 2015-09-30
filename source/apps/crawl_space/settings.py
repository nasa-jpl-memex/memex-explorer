"""Crawl settings."""

import os, sys

"""
Inserts path to project root into sys.path of of crawl_supervisor.

Splits the directory path to this settings file, and cuts off the path up
to the root of the project directory, allowing crawl_supervisor to import
modules from other apps.
"""
sys.path.insert(1, '/'.join(os.path.dirname(__file__).split('/')[:-2]))

"""
Ensures that the settings module used by crawl_supervisor is the one
used by the rest of the apps in the project.
"""
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "memex.settings")

import django
from django.conf import settings

resources_dir = settings.MEDIA_ROOT

crawl_resources_dir = os.path.join(settings.BASE_DIR, "resources")

# ACHE language detection files.
# TODO Investigate using conda-installed ACHE resources.
LANG_DETECT_PATH = os.path.join(crawl_resources_dir, 'profiles')

CCA_PATH = os.path.join(resources_dir, 'cca')
CRAWL_PATH = os.path.join(resources_dir, 'crawls')
MODEL_PATH = os.path.join(resources_dir, 'models')
CONFIG_PATH = os.path.join(crawl_resources_dir, 'configs')
IMAGES_PATH = os.path.join(resources_dir, 'images')

# Directory to store seed files temporary. See `Crawl.save()` in
#   `crawl_space.models`
SEEDS_TMP_DIR = os.path.join(resources_dir, 'seeds_tmp')
MODELS_TMP_DIR = os.path.join(resources_dir, 'models_tmp')

#Location of SOLR instance
SOLR_URL = "http://localhost:8983/solr/"
