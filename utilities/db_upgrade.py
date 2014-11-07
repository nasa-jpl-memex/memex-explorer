#!flask/bin/python

# todo: fix with proper manage.py script
# need for some version of python?
import sys
sys.path.insert(0,".")

from migrate.versioning import api
from app.config import SQLALCHEMY_DATABASE_URI
from app.config import SQLALCHEMY_MIGRATE_REPO

api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print('Current database version: ' + str(v))
