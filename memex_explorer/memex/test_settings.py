"""
Test settings for memex project.

"""
import warnings
import exceptions
import os

# Use default settings, overriding only those deemed necessary
from .settings import *

PROJECT_PATH = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[:-1])

MEDIA_ROOT = os.path.join(BASE_DIR, 'test_resources')

MEDIA_URL = '/test_resources/'

TEST_CRAWL_DATA = PROJECT_PATH + os.path.join(MEDIA_URL, "test_crawl_data")

# Ignore (particular) warnings
# ============================

# RuntimeWarning:
#   SQLite received a naive datetime (2012-11-02 11:20:15.156506)
#   while time zone support is active.
# http://stackoverflow.com/questions/11708821/
#                         django-ipython-sqlite-complains-about-naive-datetime
warnings.filterwarnings("ignore", category=exceptions.RuntimeWarning,
                        module='django.db.backends.sqlite3.base', lineno=63)
