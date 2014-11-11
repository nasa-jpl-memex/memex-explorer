#!flask/bin/python

# todo: fix with proper manage.py script
# need for some version of python?
import sys
sys.path.insert(0,".")

from migrate.versioning import api
from app.config import SQLALCHEMY_DATABASE_URI
from app.config import SQLALCHEMY_MIGRATE_REPO
from app import db
import os.path

db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))
