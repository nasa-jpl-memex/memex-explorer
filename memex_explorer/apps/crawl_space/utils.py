import os
import errno

from base.models import Project
from apps.crawl_space.models import Crawl

def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)

def rm_if_exists(filename):
    try:
        os.remove(filename)
        return True
    except OSError as e:
        if e.errno != errno.ENOENT: # (no such file or directory)
            raise
        return False

def get_crawl(project_slug, crawl_slug):
    project = Project.objects.get(slug=project_slug)
    crawl = Crawl.objects.get(project=project, slug=crawl_slug)
    return crawl
