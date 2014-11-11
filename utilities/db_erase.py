# todo: fix with proper manage.py script
# need for some version of python?
import sys
sys.path.insert(0,".")

from app import db
from app.models import DataSource

datasources = DataSource.query.all()
for d in datasources:
    db.session.delete(d)

db.session.commit()
