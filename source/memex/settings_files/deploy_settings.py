"""
Django settings for deploying memex project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from common_settings import *
HOSTNAME='explorer.continuum.io'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0#t((zq66&3*87djaltu-pn34%0p!*v_332f2p!$2i)w5y17f8'

MEDIA_ROOT = '/home/vagrant/resources'
PROJECT_PATH = os.path.join(MEDIA_ROOT, "projects")

CELERYD_USER="vagrant"
CELERYD_GROUP="vagrant"

DEPLOYMENT = True

#Must match the urls given in deploy/nginx.conf
EXTERNAL_APP_LOCATIONS = {
    'kibana': '/kibana/',
    'logio': '/logio/',
}
