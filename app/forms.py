from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, ValidationError, SelectField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email

from plotting import PLOT_TYPES


class CrawlForm(Form):
    name = StringField('Name', validators = [DataRequired()])
    description = TextAreaField('Description')
    crawler = SelectField('Crawler', choices=[('nutch','Nutch'), \
                         ('achenyu','ACHENYU')],
                          validators=[DataRequired()])
    config = FileField('Configuration', validators=[DataRequired()])
    seeds_list = FileField('Seeds List', validators=[DataRequired()])
    data_model = SelectField('Data Model')


class MonitorDataForm(Form):
    name = StringField('Name', validators = [DataRequired()])
    data_uri = StringField('Data URI', validators = [DataRequired()])
    description = TextAreaField('Description')


class DashboardForm(Form):
    name = StringField('Name', validators = [DataRequired()])
    description = TextAreaField('Description')


class PlotForm(Form):
    name = StringField('Name', validators = [DataRequired()])
    description = TextAreaField('Description')
    plot = SelectField('Plot', choices=PLOT_TYPES, validators = [DataRequired()])


class ContactForm(Form):
    name = StringField('Name', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    description = TextAreaField('Name', validators = [DataRequired()])


class ProjectForm(Form):
    name = StringField('Name', validators = [DataRequired()])
    description = TextAreaField('Description')
    icon = StringField('Icon')

class DataModelForm(Form):
    name = FileField('Name', validators=[DataRequired()])
