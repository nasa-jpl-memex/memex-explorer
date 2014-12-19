"""Main views for memex-explorer application"""
from __future__ import absolute_import, division, print_function

#  IMPORTS 
# =========

# Standard Library
# ----------------

import os
import logging
import json
import datetime as dt
import subprocess

# Third-party Libraries 
# ---------------------

from flask import (redirect, flash, render_template, request, url_for,
                   send_from_directory, jsonify, session, abort)
from werkzeug import secure_filename
from webhelpers import text

from blaze import resource, discover, Data, into, compute
from pandas import DataFrame
from bokeh.plotting import ColumnDataSource

# Local Imports
# -------------

from . import app, db
from .models import Crawl, DataSource, Dashboard, Plot, Project, Image, \
                    DataModel
from .db_api import (get_project, get_crawl, get_crawls, get_dashboards,
                     get_images, get_image, get_matches, db_add_crawl,
                     db_init_ache, get_crawl_model, get_models, get_image_space)

from .rest_api import api

from .forms import CrawlForm, MonitorDataForm, PlotForm, ContactForm, \
                    DashboardForm, ProjectForm, DataModelForm, EditProjectForm, \
                    EditCrawlForm
from .mail import send_email

from .config import ADMINS, DEFAULT_MAIL_SENDER, BASEDIR, SEED_FILES, \
                    CONFIG_FILES, MODEL_FILES, CRAWLS_PATH

from .auth import requires_auth
from .plotting import plot_builder
from .crawls import AcheCrawl, NutchCrawl


from .viz.domain import Domain
from .viz.harvest import Harvest
from .viz.harvest_rate import HarvestRate
# from .viz.termite import Termite


# Dictionary of crawls by key(project_name-crawl_name)
CRAWLS_RUNNING = {}


@app.context_processor
def context():
    """Inject some context variables useful across templates.
    See http://flask.pocoo.org/docs/0.10/templating/#context-processors
    """

    context_vars = {}

    if request.view_args and 'project_name' in request.view_args:
        project_name = request.view_args['project_name']
        project = get_project(project_name)
        if not project:
            return {}
            # flash("Project '%s' was not found." % project_name, 'error')
            # abort(404)

        crawls = get_crawls(project.id)
        dashboards = get_dashboards(project.id)
        models = get_models()
        images = get_image_space(project.id)


        context_vars.update(dict(
            project=project, crawls=crawls, dashboards=dashboards, \
            models=models, images=images))

    # All pages should (potentially) be able to present all projects
    context_vars.update(projects=Project.query.all())

    return context_vars


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def application_error(e):
    # TODO
    # http://flask.pocoo.org/docs/0.10/errorhandling/#application-errors

    # sender = DEFAULT_MAIL_SENDER
    # send_email(subject=subject, sender=sender, recipients=ADMINS, text_body=text_body, html_body=text_body)
    return render_template('500.html'), 500


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(BASEDIR, 'static'),
                               'favicon.ico', mimetype='image/x-icon')


@app.route('/')
def index():
    return render_template('index.html')


# Project
# -----------------------------------------------------------------------------

@app.route('/<project_name>')
def project(project_name):

    # return render_template('project.html', project=project, crawls=crawls,
    #                                        dashboards=dashboards)

    # `project`, `crawls`, and `dashboards` handled by the context processor.
    #   See `context() defined above.`
    return render_template('project.html')


@app.route('/<project_name>/delete', methods=['POST'])
def delete_project(project_name):
    project = get_project(project_name)
    db.session.delete(project)
    db.session.commit()
    flash('%s has successfully been deleted.' % project.name, 'success')
    return redirect(url_for('index'))


@app.route('/<project_name>/edit', methods=['POST', 'GET'])
def edit_project(project_name):
    form = EditProjectForm()
    project = get_project(project_name)
    original_name = project.name
    if form.validate_on_submit():
        if form.name.data:
            project.name = form.name.data
        if form.description.data:
            project.description = form.description.data
        if form.icon.data:
            project.icon = form.icon.data
        db.session.commit()
        flash('%s has successfully been edited.' % original_name, 'success')
        return redirect(url_for('index'))
    return render_template("edit_project.html", form=form)


@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
    form = ProjectForm(request.form)

    if form.validate_on_submit():
        project = Project(name=form.name.data, description=form.description.data, \
                        icon=form.icon.data)
        db.session.add(project)
        db.session.commit()
        flash("Project '%s' was successfully registered" % project.name, 'success')
        return redirect(url_for('project', project_name=project.name))

    return render_template('add_project.html', form=form)


# Crawl
# -----------------------------------------------------------------------------

@app.route('/<project_name>/add_crawl', methods=['GET', 'POST'])
def add_crawl(project_name):
    form = CrawlForm()
    if form.validate_on_submit():
        seed_filename = secure_filename(form.seeds_list.data.filename)
        form.seeds_list.data.save(SEED_FILES + seed_filename)
        # TODO allow upload configuration
        #config_filename = secure_filename(form.config.data.filename)
        #form.config.data.save(CONFIG_FILES + config_filename)
        project = get_project(project_name)
        crawl = db_add_crawl(project, form, seed_filename)
        subprocess.Popen(['mkdir', os.path.join(CRAWLS_PATH, crawl.name)])

        if crawl.crawler == 'ache':
            db_init_ache(project, crawl)

        else: 
            #TODO add db_init_nutch
            pass

        flash('%s has successfully been registered!' % form.name.data, 'success')
        return redirect(url_for('crawl', project_name=get_project(project_name),
                                         crawl_name=form.name.data))

    return render_template('add_crawl.html', form=form)


@app.route('/<project_name>/add_model', methods=['GET', 'POST'])
def add_model(project_name):
    form = DataModelForm()
    if form.validate_on_submit():
        registered_model = DataModel.query.filter_by(name=form.name.data).first()
        if registered_model:
            flash('Data model name already exists, please choose another name', 'error')
            return render_template('add_data_model.html', form=form)
        files = request.files.getlist("files")
        os.mkdir(MODEL_FILES + form.name.data)
        for x in files:
            x.save(MODEL_FILES + form.name.data + '/' + x.filename)
        model = DataModel(name=form.name.data,
                          filename=MODEL_FILES + form.name.data)

        db.session.add(model)
        db.session.commit()
        flash('Model has successfully been registered!', 'success')
        return redirect(url_for('project', 
                                project_name=get_project(project_name).name))

    return render_template('add_data_model.html', form=form)


@app.route('/<project_name>/crawls')
def crawls(project_name):
    return render_template('crawls.html')


@app.route('/<project_name>/crawls/<crawl_name>')
def crawl(project_name, crawl_name):
    project = get_project(project_name)
    crawl = get_crawl(crawl_name)

    if not project:
        flash("Project '%s' was not found." % project_name, 'error')
        abort(404)
    elif not crawl:
        flash("Crawl '%s' was not found." % crawl_name, 'error')
        abort(404)

    return render_template('crawl.html', crawl=crawl)


@app.route('/<project_name>/crawls/<crawl_name>/delete', methods=['POST'])
def delete_crawl(project_name, crawl_name):
    crawl = get_crawl(crawl_name)
    db.session.delete(crawl)
    db.session.commit()
    flash('%s has successfully been deleted.' % crawl.name, 'success')
    return redirect(url_for('project', project_name=project_name))


@app.route('/<project_name>/crawls/<crawl_name>/edit', methods=['POST', 'GET'])
def edit_crawl(project_name, crawl_name):
    project = get_project(project_name)
    crawl = Crawl.query.filter_by(project_id=project.id, name=crawl_name).first()
    form = EditCrawlForm()
    if form.validate_on_submit():
        if form.name.data:
            crawl.name = form.name.data
        if form.description.data:
            crawl.description = form.description.data
        if form.crawler.data == 'nutch':
            crawl.crawler = form.crawler.data
            crawl.data_model_id = ''
        elif form.crawler.data == 'ache':
            crawl.crawler = form.crawler.data
        if form.seeds_list.data: 
            seed_filename = secure_filename(form.seeds_list.data.filename)
            form.seeds_list.data.save(SEED_FILES + seed_filename)
            crawl.seeds_list = SEED_FILES + seed_filename
        if form.data_model.data:
            crawl.data_model_id = form.data_model.data.id
        db.session.commit()
        flash('%s has successfully been changed.' % crawl.name, 'success')
        return redirect(url_for('project', project_name=project_name))

    return render_template('edit_crawl.html', form=form)


@app.route('/<project_name>/crawls/<crawl_name>/run', methods=['POST'])
def run_crawl(project_name, crawl_name):
    key = project_name + '-' + crawl_name
    if CRAWLS_RUNNING.has_key(key):
        return "Crawl is already running."
    else:
        crawl = get_crawl(crawl_name)
        seeds_list = crawl.seeds_list
        if crawl.crawler=="ache":
            model = get_crawl_model(crawl)
            crawl_instance = AcheCrawl(crawl_name=crawl.name, seeds_file=seeds_list, model_name=model.name,
                                       conf_name=crawl.config)
            pid = crawl_instance.start()
            CRAWLS_RUNNING[key] = crawl_instance
            return "Crawl %s running" % crawl.name
        elif crawl.crawler=="nutch":
            crawl_instance = NutchCrawl(seed_dir=seeds_list, crawl_dir=crawl.name)
            pid = crawl_instance.start()
            CRAWLS_RUNNING[key] = crawl_instance
            return "Crawl %s running" % crawl.name
        else:
            abort(400)


@app.route('/<project_name>/crawls/<crawl_name>/stop', methods=['POST'])
def stop_crawl(project_name, crawl_name):
    key = project_name + '-' + crawl_name
    crawl_instance = CRAWLS_RUNNING.get(key)
    if crawl_instance is not None:
        crawl_instance.stop()
        del CRAWLS_RUNNING[key]
        return "Crawl stopped"
    else:
        abort(400)


@app.route('/<project_name>/crawls/<crawl_name>/refresh', methods=['POST'])
def refresh(project_name, crawl_name):

    domain_plot = Plot.query.filter_by(name='domain').first()

    # TODO retrieve data from db. These are only valid if crawler==ache.
    crawled_data_uri = os.path.join(CRAWLS_PATH, crawl_name, 'data/data_monitor/crawledpages.csv')
    relevant_data_uri = os.path.join(CRAWLS_PATH, crawl_name, 'data/data_monitor/relevantpages.csv')
    frontier_data_uri = os.path.join(CRAWLS_PATH, crawl_name, 'data/data_monitor/frontierpages.csv')
    domain_sources = dict(crawled=crawled_data_uri, relevant=relevant_data_uri, frontier=frontier_data_uri)

    domain = Domain(domain_sources, domain_plot)
    domain.push_to_server()

    harvest_plot = Plot.query.filter_by(name='harvest').first()

    harvest_data_uri = os.path.join(CRAWLS_PATH, crawl_name, 'data/data_monitor/harvestinfo.csv')
    harvest_sources = dict(harvest=harvest_data_uri)
    harvest = Harvest(harvest_sources, harvest_plot)

    harvest.push_to_server()

    return "pushed"


@app.route('/<project_name>/crawls/<crawl_name>/dashboard')
def view_plots(project_name, crawl_name):

    crawl = Crawl.query.filter_by(name=crawl_name).first()

    key = project_name + '-' + crawl_name

    # Domain
    plot = Plot.query.filter_by(name=key + '-' + 'domain').first()

    #TODO use db_api
    crawled_data_uri = os.path.join(CRAWLS_PATH, crawl_name, 'data/data_monitor/crawledpages.csv')
    relevant_data_uri = os.path.join(CRAWLS_PATH, crawl_name, 'data/data_monitor/relevantpages.csv')
    frontier_data_uri = os.path.join(CRAWLS_PATH, crawl_name, 'data/data_monitor/frontierpages.csv')
    domain_sources = dict(crawled=crawled_data_uri, relevant=relevant_data_uri, frontier=frontier_data_uri)

    domain = Domain(domain_sources, plot)
    domain_tag, source_id = domain.create_and_store()

    plot.source_id = source_id
    ###


    # Harvest

    plot = Plot.query.filter_by(name='harvest').first()

    harvest_data_uri = os.path.join(CRAWLS_PATH, crawl_name, 'data/data_monitor/harvestinfo.csv')

    harvest_sources = dict(harvest=harvest_data_uri)

    harvest = Harvest(harvest_sources, plot)
    harvest_tag, source_id = harvest.create_and_store()

    plot.source_id = source_id
    ###

    db.session.flush()
    db.session.commit()

    return render_template('dash.html', plots=[domain_tag, harvest_tag], crawl=crawl)


@app.route('/<project_name>/crawls/<crawl_name>/status', methods=['GET'])
def status_crawl(project_name, crawl_name):
    key = project_name + '-' + crawl_name
    crawl_instance = CRAWLS_RUNNING.get(key)
    if crawl_instance is not None:
        return crawl_instance.status()
    else:
        return "Stopped"


# Image Space
# -----------------------------------------------------------------------------

@app.route('/<project_name>/crawls/<crawl_name>/image_space')
def image_space(project_name, crawl_name):
    project = Project.query.filter_by(name=project_name).first()
    crawl = Crawl.query.filter_by(name=crawl_name).first()
    crawls = Crawl.query.filter_by(project_id=project.id)
    dashboards = Dashboard.query.filter_by(project_id=project.id)
    if not crawl:
        flash("Crawl '%s' was not found." % crawl_name, 'error')
        abort(404)
    elif not project:
        flash("Project '%s' was not found." % project_name, 'error')
        abort(404)
    elif crawl.project_id != project.id:
        flash("This crawl is not part of project '%s'" % project_name, 'error')
        abort(404)
    return render_template('crawl.html', project=project, crawl=crawl,\
                            crawls=crawls, dashboards=dashboards)


# Plot & Dashboard
# -----------------------------------------------------------------------------

@app.route('/<project_name>/add_dashboard', methods=['GET', 'POST'])
def add_dashboard(project_name):
    project = Project.query.filter_by(name=project_name).first()
    crawls = Crawl.query.filter_by(project_id=project.id)
    dashboards = Dashboard.query.filter_by(project_id=project.id)
    form = DashboardForm(request.form)

    if form.validate_on_submit():
        data = Dashboard(name=form.name.data, description=form.description.data, \
                        project_id=project.id)
        db.session.add(data)
        db.session.commit()
        flash("Dashboard '%s' was successfully registered" % form.name.data, 'success')
        return redirect(url_for('dash', project_name=project.name, \
                        dashboard_name=form.name.data))

    return render_template('add_dashboard.html', project=project, crawls=crawls,
                            form=form, dashboards=dashboards)


@app.route('/<project_name>/dashboards/<dashboard_name>')
def dash(project_name, dashboard_name):
    project = Project.query.filter_by(name=project_name).first()
    crawls = Crawl.query.filter_by(project_id=project.id)
    dashboards = Dashboard.query.filter_by(project_id=project.id)
    dashboard = Dashboard.query.filter_by(name=dashboard_name).first()
    plots = Plot.query.filter_by(project_id=project.id)
    if not dashboard:
        flash("Dashboard '%s' was not found." % dashboard_name, 'error')
        abort(404)
    elif not project:
        flash("Project '%s' was not found." % project_name, 'error')
        abort(404)
    elif dashboard.project_id != project.id:
        flash("Dashboard is not part of project '%s'." % project_name, 'error')
        abort(404)

    return render_template('dash.html', project=project, crawls=crawls, \
                           dashboards=dashboards, dashboard=dashboard, plots=plots)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm(request.form)
    crawls = Crawl.query.all()

    if form.validate_on_submit():
        subject = ' -- '.join([form.issue.data, form.name.data])
        sender = DEFAULT_MAIL_SENDER
        text_body = form.description.data
        send_email(subject=subject, sender=sender, recipients=ADMINS,
                   text_body=text_body, html_body=text_body)
        flash('Thank you for contacting us! We will be in touch shortly.', 'success')
        return redirect(url_for('index'))

    return render_template('contact.html', form=form)


# Compare (Image Space)
# ------------------------------------------------------------------------

@app.route('/<project_name>/image_space/<image_id>/compare/')
def compare(project_name, image_id):

    project = get_project(project_name)
    images = get_images(project.id)

    img = get_image(image_id)

    exif_info = dict(zip(('EXIF_BodySerialNumber', 'EXIF_LensSerialNumber',
              'Image_BodySerialNumber', 'MakerNote_InternalSerialNumber',
              'MakerNote_SerialNumber', 'MakerNote_SerialNumberFormat'),

             (img.EXIF_BodySerialNumber, img.EXIF_LensSerialNumber,
              img.Image_BodySerialNumber, img.MakerNote_InternalSerialNumber,
              img.MakerNote_SerialNumber, img.MakerNote_SerialNumberFormat)))

    # serial_matches = get_info_serial(img.EXIF_BodySerialNumber)
    # full_match_paths = [app.config['STATIC_IMAGE_DIR'] + x.img_file for x in serial_matches
    #                                                                  if x.Uploaded != 1]
    # internal_matches = [(x.split('/static/')[-1], x.split('/')[-1])
    #                         for x in full_match_paths]

    internal_matches = get_matches(project.id, img.id)
    for x in internal_matches:
        if (img.id, x.id) in app.MATCHES:
            x.match = "true"
        else:
            x.match = "false"

    # if img.EXIF_BodySerialNumber:
    #     external_matches = lost_camera_retreive(img.EXIF_BodySerialNumber)
    # else:
    #     external_matches = []

    return render_template('compare.html', image=img, exif_info=exif_info, 
                            internal_matches=internal_matches,
                            # external_matches=external_matches
                             )

@app.route('/static/image/<image_id>')
def image_source(image_id):
    img_dir = os.path.join(BASEDIR,
                                   'image')

    img_filename = "%s.jpg" % image_id
    print(img_dir, img_filename)

    return send_from_directory(img_dir, img_filename)


@app.route('/<project_name>/image_space/<image_id>')
def inspect(project_name, image_id):
    img = get_image(image_id)

    exif_info = dict(zip(('EXIF_BodySerialNumber', 'EXIF_LensSerialNumber',
              'Image_BodySerialNumber', 'MakerNote_InternalSerialNumber',
              'MakerNote_SerialNumber', 'MakerNote_SerialNumberFormat'),

             (img.EXIF_BodySerialNumber, img.EXIF_LensSerialNumber,
              img.Image_BodySerialNumber, img.MakerNote_InternalSerialNumber,
              img.MakerNote_SerialNumber, img.MakerNote_SerialNumberFormat)))

    return render_template('inspect.html', image=img, exif_info=exif_info)

