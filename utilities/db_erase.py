from app import db
from app.models import DataSource

datasources = DataSource.query.all()
for d in datasources:
    db.session.delete(d)

db.session.commit()