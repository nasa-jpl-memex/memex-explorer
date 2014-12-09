from . import db
from .models import Project, Crawl, Dashboard

def get_project(project_name):
    """Return the project identified by `project_name`.
    """
    return Project.query.filter_by(name=project_name).first()


def get_crawl(project_id, crawl_name):
    """Return the first crawl under `project_id` that matches `crawl_name`.
    """
    return Crawl.query.filter_by(project_id=project_id, name=crawl_name).first()


def get_crawls(project_id):
    """Return all crawls that match `project_id`.
    """
    return Crawl.query.filter_by(project_id=project_id)


def get_dashboards(project_id):
    """Return all dashboards that match `project_id`.
    """
    return Dashboard.query.filter_by(project_id=project_id)


def get_images(project_id):
    """Return all images under `project_id` that match `crawl_name`.
    """
    return Image.query.filter_by(project_id=project_id)



def get_images(image_id):
    """Return the image that matches `image_id`.
    """
    return Image.query.filter_by(id=image_id).first()