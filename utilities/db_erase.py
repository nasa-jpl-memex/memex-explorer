# todo: fix with proper manage.py script
# need for some version of python?
import sys
sys.path.insert(0,".")

from app import db
from app.models import Crawl

crawls = Crawl.query.all()
for d in crawls:
    db.session.delete(d)

db.session.commit()
