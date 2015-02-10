"""Crawl Supervisor is a free-standing script that monitors and logs output
from crawl processes.

At the moment, this is a thin wrapper for the purpose of development. In
production systems, this application should call out to a job queueing
library managing crawl processes on distributed systems.


Example
-------

    $ python crawl_supervisor.py --project project_slug --crawl crawl_slug

"""

import argparse
import inspect

from base.models import Project
from apps.crawl_space.models import Crawl
from apps.crawl_space.crawls import AcheCrawl, NutchCrawl


def parse_args():
    """Helper function to parse command line arguments.

    Arguments
    ---------

    -p, --project : str, required
        Project slug
    -c, --crawl : str, required
        Crawl slug

    Returns
    -------

    argparse.Namespace    
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--project", dest="project_slug", type=str,
                        required=True, help="Project slug")
    parser.add_argument("-c", "--crawl", dest="crawl_slug", type=str,
                        required=True, help="Crawl slug")
    return parser.parse_args()


def get_crawl(project_slug, crawl_slug):
    return Crawl.objects.get(project=Project.objects.get(slug=project_slug),
                             slug=crawl_slug)


class CrawlSupervisor(object):

    def __init__(self, *args, **kwargs):

        c = self.crawl_model = get_crawl(kwargs['project_slug'], kwargs['crawl_slug'])
        if c.crawler == 'ache':
            self.crawl = AcheCrawl(c)

        elif c.crawler == 'nutch':
            self.crawl = NutchCrawl(c)

    def start(self):
        self.crawl.run()


if __name__ == "__main__":

    import django
    django.setup()

    args = parse_args()
    crawl_supervisor = CrawlSupervisor(**vars(args))
    crawl_supervisor.start()
