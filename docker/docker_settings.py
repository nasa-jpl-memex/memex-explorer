"""
Django settings for memex project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from common_settings import *
import os

# SECURITY WARNING: Not setting VIRTUAL_HOST prevents Django from being able to verify headers
ALLOWED_HOSTS = [os.environ.get('VIRTUAL_HOST', '*')]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0#t((zq66&3*87djaltu-pn34%0p!*v_332f2p!$2i)w5y17f8'

# SECURITY WARNING: don't run with debug turned on in production!
PRODUCTION = os.environ.get('PRODUCTION', False)

# when INLINE is true point to local sources for changes/documentation instead of remote ones
INLINE = os.environ.get('INLINE', False)

if PRODUCTION:
    DEBUG = False
    TEMPLATE_DEBUG = False
    DEPLOYMENT = True
else:
    DEBUG = True
    TEMPLATE_DEBUG = True
    INSTALLED_APPS += ('debug_toolbar',)
    DEPLOYMENT = False


MEDIA_ROOT = os.path.join(BASE_DIR, 'resources')
PROJECT_PATH = os.path.join(MEDIA_ROOT, "projects")

VIRTUAL_HOST = os.environ.get('VIRTUAL_HOST', 'localhost')
PROTOCOL = os.environ.get('HTTP_PROTOCOL', 'http')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',)
}

# ddt is treated as an external service for now

EXTERNAL_APP_LOCATIONS = {
    'bokeh-server': '/bokeh',
    'ddt': PROTOCOL + '://' + VIRTUAL_HOST + ':8084',
    'tad': '/tad',
    'kibana': '/kibana',
}
