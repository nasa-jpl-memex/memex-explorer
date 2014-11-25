"""
Testing prper rendering of front page
"""

import os
import sys
sys.path.insert(0, ".")
import unittest

from app import app, db
from app.config import basedir

TESTDB = 'test_app.db'
TESTDB_SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, TESTDB)


class ServerUpTest(unittest.TestCase):

    def setUp(self):
        app.testing = True
        app.port = 8943
        with app.app_context():

            self.app = app.test_client()
            self.db = TESTDB_SQLALCHEMY_DATABASE_URI

    def test_get_test(self):
        """Does hitting the /test endpoint return the proper HTTP code?"""
        response = self.app.get('/')
        assert response.status_code == 200

    def test_title(self):
        """test title of root page"""
        rv = self.app.get('/')
        self.assertIn('MEMEX VIEWER', rv.data)
