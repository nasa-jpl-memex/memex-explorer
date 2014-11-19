"""
Testing DB Insertions of Crawl data
"""

import os
import sys
sys.path.insert(0, ".")
import unittest

from app import app, db
from app.config import basedir

TESTDB = 'test_app.db'
TESTDB_SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, TESTDB)


class RegisterCrawlTest(unittest.TestCase):

    def setUp(self):
        app.testing = True
        app.port = 8943
        app.config['WTF_CSRF_ENABLED'] = False
        with app.app_context():

            self.app = app.test_client()
            self.db = TESTDB_SQLALCHEMY_DATABASE_URI

    def test_page(self):
        """test page exists"""
        response = self.app.get('/register_crawl')
        assert response.status_code == 200

    def test_no_data(self):
        """test error handling of no data being supplied during submit"""

        rv = self.app.get('/')
        data = {}

        # Bad Post is still a 200 OK
        rv = self.app.post('/register_crawl', data=data, follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn("This field is required.", rv.data)

    def test_partial_data(self):
        """test error handling of partial data in form"""

        rv = self.app.get('/')
        data = {"description": "test test"}

        # Posting bad data should still generate a 200 OK
        rv = self.app.post('/register_crawl', data=data, follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn("This field is required.", rv.data)

    def test_insert_data(self):
        """test proper insertion"""

        rv = self.app.get('/')
        data = {"description": "DESCRIPTION", "name": "UNIQUETITLE"}

        rv = self.app.post('/register_crawl', data=data, follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn("UNIQUETITLE", rv.data)

        # Posting bad data should still generate a 200 OK
        rv = self.app.get('/',)
        self.assertEqual(rv.status_code, 200)
        self.assertIn("UNIQUETITLE", rv.data)

    def test_duplicate_insert(self):
        """test error handling of duplicate data"""

        rv = self.app.get('/')

        data = {"description": "DESCRIPTION", "name": "UNIQUETITLE"}

        # Posting bad data should still generate a 200 OK
        rv = self.app.post('/register_crawl', data=data)
        self.assertEqual(rv.status_code, 200)
        self.assertIn("has already been registered-please provide another name.", rv.data)
