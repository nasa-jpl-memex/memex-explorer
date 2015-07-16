"""
Test settings for memex project.

"""
import warnings
import exceptions
import os

# Use default settings, overriding only those deemed necessary
from .settings import *

MEDIA_ROOT = os.path.join(BASE_DIR, 'test_resources')

MEDIA_URL = '/test_resources/'

DEPLOYMENT = False

TEST_CRAWL_DATA = os.path.join(MEDIA_ROOT, "test_crawl_data")

LANG_DETECT_PATH = os.path.join(MEDIA_ROOT, 'profiles')

CONFIG_PATH = os.path.join(MEDIA_ROOT, 'configs')

CCA_PATH = os.path.join(MEDIA_ROOT, 'cca')

CRAWL_PATH = os.path.join(MEDIA_ROOT, 'crawls')

MODEL_PATH = os.path.join(MEDIA_ROOT, 'models')

IMAGES_PATH = os.path.join(MEDIA_ROOT, 'images')

SEEDS_TMP_DIR = os.path.join(MEDIA_ROOT, 'seeds_tmp')

MODELS_TMP_DIR = os.path.join(MEDIA_ROOT, 'models_tmp')

TESTING = True

# Ignore (particular) warnings
# ============================

# RuntimeWarning:
#   SQLite received a naive datetime (2012-11-02 11:20:15.156506)
#   while time zone support is active.
# http://stackoverflow.com/questions/11708821/
#                         django-ipython-sqlite-complains-about-naive-datetime
warnings.filterwarnings("ignore", category=exceptions.RuntimeWarning,
                        module='django.db.backends.sqlite3.base', lineno=63)
