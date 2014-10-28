from __future__ import absolute_import

import os

from webhelpers import text

from flask import redirect, flash, render_template, request, url_for, send_from_directory, jsonify, session

from werkzeug import secure_filename
from .models import Crawl, MonitorData, Dashboard, Plot
from .forms import CrawlForm, DashboardForm, MonitorDataForm, DashboardForm, PlotForm, ContactForm


from . import app, db
from blaze import resource, discover, Data, into, compute
import json
from pandas import DataFrame
import datetime as dt
from .mail import send_email
from .config import ADMINS, DEFAULT_MAIL_SENDER
from .auth import requires_auth

from bokeh.plotting import ColumnDataSource


@app.context_processor
def inject_crawls():
    crawls = Crawl.query.all()
    plots = Plot.query.all()
    dashboards = Dashboard.query.all()
    return dict(crawls=crawls, plots=plots, dashboards=dashboards)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/register_crawl', methods=['GET', 'POST'])
def register():
    form = CrawlForm(request.form)

    if request.method == 'POST' and form.validate():
        endpoint = text.urlify(form.name.data)
        crawl = Crawl(name = form.name.data, endpoint = endpoint, data_location = form.data_location.data, \
            description = form.description.data)
        registered_crawl = crawl.query.filter_by(name=form.name.data).first()

        if registered_crawl:
            flash('Crawl name already registered, please choose another name', 'error')
            return render_template('register_crawl.html', form=form)

        db.session.add(crawl)
        db.session.commit()
        flash('Your data source was successfully registered', 'success')
        return redirect('/index')
    return render_template('register_crawl.html', form=form)


@app.route('/crawl/<crawl_endpoint>')
def crawl(crawl_endpoint):
    crawl = Crawl.query.filter_by(endpoint=crawl_endpoint).first()
    data = crawl.monitor_data.all()
    plots = crawl.plots
    dashbs = crawl.dashboards
    data_list = []
    plot_list = []
    dash_list = []
    for d in data:
        data_list.append({"name": d.name,"endpoint": d.endpoint})
    for p in plots:
        plot_list.append({"name": p.name,"endpoint": p.endpoint})
    for d in dashbs:
        dash_list.append({"name": d.name,"endpoint": d.endpoint})
    if crawl == None:
        flash('Crawl %s not found.' % crawl.name)
        return redirect(url_for('index'))
    return render_template('crawl.html', crawl=crawl, data_list=data_list, plot_list=plot_list, dash_list=dash_list)


@app.route('/crawl/<crawl_endpoint>/register_data', methods=['GET', 'POST'])
def register_data(crawl_endpoint):
    crawl = Crawl.query.filter_by(endpoint=crawl_endpoint).first()
    form = MonitorDataForm(request.form)

    if request.method == 'POST' and form.validate():
        endpoint = text.urlify(form.name.data)
        data = MonitorData(name = form.name.data, endpoint = endpoint, data_uri = form.data_uri.data, \
            description = form.description.data, crawl=crawl)
        registered_data= crawl.query.filter_by(name=form.name.data).first()

        if registered_data:
            flash('MonitorData name already registered, please choose another name', 'error')
            return render_template('register_data.html', form=form)

        db.session.add(data)
        db.session.commit()
        flash('Your monitor data was successfully registered', 'success')
        return redirect('/index')
    return render_template('register_data.html', crawl=crawl, form=form)


@app.route('/crawl/<crawl_endpoint>/data/<data_endpoint>')
def data(crawl_endpoint, data_endpoint):
    crawl = Crawl.query.filter_by(endpoint=crawl_endpoint).first()
    monitor_data = MonitorData.query.filter_by(crawl_id=crawl.id,endpoint=data_endpoint).first()

    plots = monitor_data.plots
    plot_list = []
    for p in plots:
        plot_list.append({"name": p.name,"endpoint": p.endpoint})

    uri = monitor_data.data_uri
    t = Data(uri)
    dshape = t.dshape
    columns = t.fields
    fields = ', '.join(columns)
    expr = t.head(10)
    df = into(DataFrame, expr)
    sample = df.to_html()

    return render_template('data.html', crawl=crawl, data=monitor_data, plots=plots, fields=fields, sample=sample, dshape=dshape) 


@app.route('/crawl/<crawl_endpoint>/data/<data_endpoint>/explore')
def data_explore(crawl_endpoint, data_endpoint):
    crawl = Crawl.query.filter_by(endpoint=crawl_endpoint).first()
    monitor_data = MonitorData.query.filter_by(crawl_id=crawl.id,endpoint=data_endpoint).first()

    plots = monitor_data.plots
    plot_list = []
    for p in plots:
        plot_list.append({"name": p.name,"endpoint": p.endpoint})

    uri = monitor_data.data_uri
    t = Data(uri)
    dshape = t.dshape
    columns = t.fields
    fields = ', '.join(columns)
    expr = t.head(10)
    df = into(DataFrame, expr)
    sample = df.to_html()

    return render_template('data_explore.html', crawl=crawl, data=monitor_data, plots=plots, fields=fields, sample=sample, dshape=dshape) 


@app.route('/plot/<plot_endpoint>')
def plot(plot_endpoint):
    plot = Plot.query.filter_by(endpoint=plot_endpoint).first()
    data = plot.data.query.all()

    return render_template('plot.html', data=data, plot=plot) 

@app.route('/plot/create_plot')
def create_plot():
    plot = Plot.query.filter_by(endpoint=plot_endpoint).first()
    data = plot.data.query.all()

    return render_template('create_plot.html', data=data, plot=plot) 


@app.route('/dashboard/<dashboard_endpoint>')
def dash(dashboard_endpoint):
    dash = Dashboard.query.filter_by(endpoint=dashboard_endpoint).first()
    plots = dash.plots
    crawls = dash.crawls.query.all()

    return render_template('dash.html', dash=dash, plot=plot, crawls=crawls) 


@app.route('/data/<data_endpoint>/edit', methods=['GET', 'POST'])
@requires_auth
def data_edit(data_endpoint):
    form = SourceForm(request.form)
    crawls = Crawl.query.all()
    datasource = Crawl.query.filter_by(endpoint=data_endpoint).first()

    description = Crawl.description
    if request.method == 'POST' and form.validate():
        db.session.add(crawl)
        crawl.name = form.name.data
        crawl.endpoint = text.urlify(form.name.data)
        crawl.uri = form.uri.data
        crawl.description = form.description.data
        crawl.datashape = form.datashape.data
        db.session.flush()
        db.session.commit()
        crawls = Crawl.query.all()
        flash('Your data source was successfully updated', 'success')
        return redirect('/data/'+ crawl.endpoint)
    return render_template('edit.html', form=form, crawl=crawl)


#@app.route('/data/<data_endpoint>/delete', methods=['GET', 'POST'])
#@requires_auth
#def data_delete(data_endpoint):
#    crawls = Crawl.query.all()
#    crawl = Crawl.query.filter_by(endpoint=data_endpoint).first()
#    dashbs = crawl.dashboards.all()
#    description = crawl.description
#    if request.method == 'POST':
#        for d in dashbs:
#            db.session.delete(d)
#        db.session.delete(crawl)
#        print "Crawl Deleted"
#       db.session.commit()
#        flash('Your data source %s was successfully deleted' % crawl.name, 'success')
#        return redirect(url_for('index'))
#    return render_template('delete.html', crawl=crawl)


#@app.route('/<data_endpoint>/dashboard/<dash_endpoint>/delete', methods=['GET', 'POST'])
#def dashboard_delete(data_endpoint, dash_endpoint):
#    crawls = Crawl.query.all()
#    crawl = Crawl.query.filter_by(endpoint=data_endpoint).first()
#    dashbs = crawl.dashboards.all()
#    dashb = crawl.dashboards.filter_by(endpoint=dash_endpoint).first()
#    if request.method == 'POST':
#        db.session.delete(dashb)
#        print "Dashboard Deleted"
#        db.session.commit()
#       flash('Your Dashboard %s was successfully deleted' % dashb.name, 'success')
#        return redirect(url_for('index'))
#    return render_template('delete_dashboard.html', crawl=crawl, dashb = dashb)


#@app.route('/data/<data_endpoint>/dashboard', methods=['GET', 'POST'])
#def create_dashboard(data_endpoint):
#    form = DashboardForm()
#    crawls = Crawl.query.all()
#    crawl = Crawl.query.filter_by(endpoint=data_endpoint).first()
#    if crawl == None:
#        flash('crawl %s not found.' % crawl.name)
#        return redirect(url_for('index'))
#
#    if request.method == 'POST' and form.validate():
#        fmt ='%Y-%m-%d-%H-%M-%S-%f' 
#        current_time = dt.datetime.now().strftime(fmt)
#        dashboard_uri = form.name.data + "_" + crawl.name + "_" + current_time
#
#        file = request.files.get('upload_file')
#
#       if file and form.plot.data == 'notebook':
#            filename = secure_filename(file.filename)
#            file.save(os.path.join(app.config['UPLOADED_NOTEBOOKS'], filename))
#            dashboard_uri = os.path.join(os.path.basename(app.config['UPLOADED_NOTEBOOKS']), filename)
#
#        dashboard_endpoint = text.urlify(form.name.data)
#        
#        dashboard = Dashboard(name = form.name.data, endpoint = dashboard_endpoint, uri = dashboard_uri, description = form.description.data, \
#            plot=form.plot.data, column_name_x=form.column_name_x.data, column_name_y=form.column_name_y.data, crawl=crawl)
#        registered_dashboard = Dashboard.query.filter_by(name=form.name.data).first()
#        # if registered_dashboard:
#        #     flash('Datashboard name already registered, please choose another name', 'error')
#        #     return redirect(url_for('create_dashboard', data_endpoint=crawl.url))
#        db.session.add(dashboard)
#        db.session.commit()
#
#        return redirect(url_for('dashboard', data_endpoint=data_endpoint, dash_endpoint=dashboard_endpoint))

#    uri = crawl.uri
#    t = Data(crawl.uri)
#    dshape = t.dshape
#    columns = t.fields
#    fields = ', '.join(columns)
#    expr = t.head(2)
#    df = into(DataFrame, expr)
#    sample = df.to_html()
#    return render_template('create_dashboard.html', dshape=dshape, crawl=crawl, fields=fields, sample=sample, form=form) 


#@app.route('/<data_endpoint>/dashboard/<dash_endpoint>')
#def dashboard(data_endpoint,dash_endpoint):
#    crawls = Crawl.query.all()
#    crawl = Crawl.query.filter_by(endpoint=data_endpoint).first()
#    dashbs = crawl.dashboards.all()
#    dashb = crawl.dashboards.filter_by(endpoint=dash_endpoint).first()
#    uri = crawl.uri
#    t = Data(crawl.uri)
#    dshape = t.dshape
#    columns = t.fields
#    fields = ', '.join(columns)
#    expr = t.head(10)
#    df = into(DataFrame, expr)
#    sample = df.to_html()

#    if dashb.plot == 'map':
        # Get columns
#        column_name_x = dashb.column_name_x
#        column_name_y = dashb.column_name_y
#        selected_columns = [column_name_x, column_name_y]
#        print column_name_x
#        table_select = t[selected_columns]
#        table = table_select.relabel({column_name_x: 'longitude', column_name_y: 'latitude'})
#        filter_nulls = table[table.longitude != None]
#        cds = into(Columncrawl, filter_nulls)
#        script, div = map_builder(cds)

#    if dashb.plot == 'timeseries':
        # Get columns
#        column_name_x = dashb.column_name_x
#        column_name_y = dashb.column_name_y
#        selected_columns = [column_name_x, column_name_y]
#        table_select = t[selected_columns]
#        table = table_select.relabel({column_name_x: 'x', column_name_y: 'y'})
#        cds = into(Columncrawl, table)
#        script, div = timeseries_builder(cds)

#    if dashb.plot == 'notebook':
#        filename = dashb.uri
#        head, div = html_export(filename)
#        return render_template('dashboard.html', script=None, div=div, crawl=crawl, dashb=dashb)

#    return render_template('dashboard.html', script=script, div=div, crawl=crawl, dashb=dashb)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm(request.form)
    crawls = Crawl.query.all()

    if request.method == 'POST' and form.validate():
        # import pdb
        # pdb.set_trace()
        subject = ' '.join([form.issue.data, form.name.data])
        sender = DEFAULT_MAIL_SENDER
        text_body = form.description.data
        send_email(subject=subject, sender=sender, recipients=ADMINS, text_body=text_body, html_body=text_body)
        print 'email sent'
        flash('Thank you for contacting Continuum! We will be in touch shortly.', 'success')
        return redirect('/index')

    data = session.get('data_uri', '')

    return render_template('contact.html', form=form, data=data)
