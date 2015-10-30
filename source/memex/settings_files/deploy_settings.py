"""
Django settings for deploying memex project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import os
import sys

from common_settings import *
HOSTNAME='explorer.continuum.io'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0#t((zq66&3*87djaltu-pn34%0p!*v_332f2p!$2i)w5y17f8'

MEDIA_ROOT = '/home/vagrant/resources'
PROJECT_PATH = os.path.join(MEDIA_ROOT, "projects")

CELERYD_USER="vagrant"
CELERYD_GROUP="vagrant"

DEPLOYMENT = True
# SECURITY - This should eventually be turned off in deployment
DEBUG = True

#Must match the urls given in deploy/nginx.conf
EXTERNAL_APP_LOCATIONS = {
    'ddt': 'http://explorer.continuum.io:8084',
    'kibana': '/kibana/',
}

# A few more checks in deployment that services are running correctly

REQUIRED_EXTERNAL_APPS = {'celery',
                          'elasticsearch',
                          'kibana',
                          'redis',
                          'tika'}

# but celery imports settings.py too, so don't check if we're celery

my_process = os.path.basename(sys.argv[0])
if my_process != 'celery':
    assert REQUIRED_EXTERNAL_APPS <= READY_EXTERNAL_APPS