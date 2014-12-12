"""RESTful API for memex-explorer application"""
from __future__ import absolute_import, division, print_function

#  IMPORTS 
# =========

# Standard Library
# ----------------


# Third-party Libraries 
# ---------------------

from flask import (request, url_for)
from flask.ext.restful import Api, Resource, reqparse

# Local Imports
# -------------

from . import app, db
from .models import Crawl, DataSource, Dashboard, Plot, Project, Image
from .db_api import (get_project, get_crawl, get_crawls, get_dashboards,
                     get_images, get_image, get_matches)
from .forms import CrawlForm, MonitorDataForm, PlotForm, ContactForm, \
                    DashboardForm, ProjectForm


api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('source_id', type=int)
parser.add_argument('match_id', type=int)
parser.add_argument('match', type=bool, help='Rate cannot be converted')

class ImageAPI(Resource):
    def post(self):
        args = parser.parse_args()
        args['source_id']
        args['match_id']
        return dict(asdf='sussess')

api.add_resource(ImageAPI, '/api/image_match/', endpoint = 'image')
