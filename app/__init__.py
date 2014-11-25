from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail

app = Flask(__name__)
app.secret_key = 'some_secret'
db = SQLAlchemy(app)

app.config.from_pyfile('config.py')
mail = Mail(app)


from app import views, models
