from . import db


project_app = db.Table('project_app',
    db.Column('project_id', db.Integer, db.ForeignKey('project.id')),
    db.Column('app_id', db.Integer, db.ForeignKey('app.id') )
)


class Project(db.Model):
    __tablename__ = "project"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.Text)
    icon = db.Column(db.String(64))
    apps = db.relationship("App", secondary=project_app, backref="projects")
    crawls = db.relationship("Crawl", backref="project")


class App(db.Model):
    __tablename__ = "app"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.Text)
    icon = db.Column(db.String(64))


data_plot = db.Table('data_plot',
    db.Column('data_source_id', db.Integer, db.ForeignKey('data_source.id')),
    db.Column('plot_id', db.Integer, db.ForeignKey('plot.id'))
)


crawl_data = db.Table('crawl_data',
    db.Column('crawl_id', db.Integer, db.ForeignKey('crawl.id')),
    db.Column('data_source_id', db.Integer, db.ForeignKey('data_source.id'))
)


crawl_images = db.Table('crawl_images',
    db.Column('crawl_id', db.Integer, db.ForeignKey('crawl.id')),
    db.Column('image_space_id', db.Integer, db.ForeignKey('image_space.id'))
)


plot_dashboard = db.Table('plot_dashboard',
    db.Column('plot_id', db.Integer, db.ForeignKey('plot.id')),
    db.Column('dashboard_id', db.Integer, db.ForeignKey('dashboard.id'))
)


class Crawl(db.Model):
    __tablename__ = "crawl"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.Text)
    crawler = db.Column(db.Text)
    config = db.Column(db.Text)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    data_sources = db.relationship('DataSource', secondary=crawl_data, \
        backref=db.backref('crawl', lazy='dynamic'))
    images = db.relationship('ImageSpace', secondary=crawl_images, \
        backref=db.backref('crawl', lazy='dynamic'))

    def __repr__(self):
        return '<Crawl %r>' % (self.name)


class DataSource(db.Model):
    __tablename__ = "data_source"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    data_uri = db.Column(db.String(120))
    description = db.Column(db.Text)
    plots = db.relationship('Plot', secondary=data_plot, \
        backref=db.backref('data', lazy='dynamic'))

    def __repr__(self):
        return '<DataSource %r>' % (self.name)


class ImageSpace(db.Model):
    __tablename__ = "image_space"
    id = db.Column(db.Integer, primary_key=True)
    images_location = db.Column(db.Text)
    description = db.Column(db.Text)

    def __repr__(self):
        return '<ImageSpace %r>' % (self.id)


class Plot(db.Model):
    __tablename__ = "plot"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.Text)
    plot = db.Column(db.String(64))


class Dashboard(db.Model):
    __tablename__ = "dashboard"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.Text)
    plots = db.relationship('Plot', secondary=plot_dashboard, \
        backref=db.backref('dashboard', lazy='dynamic'))

