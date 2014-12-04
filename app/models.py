from . import db


team_user = db.Table('team_user',
    db.Column('team_id', db.Integer, db.ForeignKey('team.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)


class Team(db.Model):
    __tablename__ = "team"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    leader_id = db.Column(db.Integer)
    users = db.relationship('User', secondary=team_user, \
        backref=db.backref('team', lazy='dynamic'))


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(12))
    email = db.Column(db.String(50))


class Project(db.Model):
    __tablename__ = "project"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
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
    data_model_id = db.Column(db.Integer, db.ForeignKey('data_model.id'))
    data_sources = db.relationship('DataSource', secondary=crawl_data, \
        backref=db.backref('crawl', lazy='dynamic'))
    images = db.relationship('ImageSpace', secondary=crawl_images, \
        backref=db.backref('crawl', lazy='dynamic'))

    def __repr__(self):
        return '<Crawl %r>' % (self.name)


class DataModel(db.Model):
    __tablename__ = "data_model"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return '<DataModel %r>' % (self.name)


class DataSource(db.Model):
    __tablename__ = "data_source"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    data_uri = db.Column(db.String(120))
    description = db.Column(db.Text)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    plots = db.relationship('Plot', secondary=data_plot, \
        backref=db.backref('data', lazy='dynamic'))

    def __repr__(self):
        return '<DataSource %r>' % (self.name)


class ImageSpace(db.Model):
    __tablename__ = "image_space"
    id = db.Column(db.Integer, primary_key=True)
    images_location = db.Column(db.Text)
    description = db.Column(db.Text)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    def __repr__(self):
        return '<ImageSpace %r>' % (self.id)


class Image(db.Model):
    __tablename__ = "image"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    img_file = db.Column(db.String(140))
    EXIF_LensSerialNumber = db.Column(db.String(140))
    MakerNote_SerialNumberFormat = db.Column(db.String(140))
    EXIF_BodySerialNumber = db.Column(db.String(140))
    MakerNote_InternalSerialNumber = db.Column(db.String(140))
    MakerNote_SerialNumber = db.Column(db.String(140))
    Image_BodySerialNumber = db.Column(db.String(140))
    Uploaded = db.Column(db.Integer)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    def __unicode__(self):
        return self.img_file


class Plot(db.Model):
    __tablename__ = "plot"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.Text)
    endpoint = db.Column(db.String(64), index=True, unique=True)
    plot = db.Column(db.String(64), index=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    source_id = db.Column(db.String(64))
    autoload_tag = db.Column(db.Text)


class Dashboard(db.Model):
    __tablename__ = "dashboard"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.Text)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    plots = db.relationship('Plot', secondary=plot_dashboard, \
        backref=db.backref('dashboard', lazy='dynamic'))

