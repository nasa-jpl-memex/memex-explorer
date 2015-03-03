import os
from abc import ABCMeta, abstractmethod

from bokeh.models import ColumnDataSource
from bokeh.plotting import Document, Session
import pandas as pd

from harvest import Harvest
from domain import Domain
from apps.crawl_space.settings import CRAWL_PATH


class PlotsNotReadyException(Exception):
    pass 


class AcheDashboard(object):

    def __init__(self, crawl):
        self.crawl = crawl
        if self.crawl.crawler != "ache":
            raise ValueError("Crawl must be using the Ache crawler.")
        self.harvest = Harvest(crawl)
        self.domain = Domain(crawl)
        self.relevant_data = self.domain.relevant_data

    def get_harvest_plot(self):
        try:
            script, div = self.harvest.create()
        except:
            return [None, None]
        return [script, div]

    def get_domain_plot(self):
        try:
            script, div = self.domain.create()
        except Exception:
            return [None, None]
        return [script, div]

    def write_relevant_seeds(self):
        urls = pd.read_csv(self.relevant_data, delimiter='\t', header=None,
                         names=['url', 'timestamp'])['url']
        return urls.to_csv(os.path.join(CRAWL_PATH, str(self.crawl.id), 'relevant_seeds.txt'),
                           index=False)

    def get_plots(self):
        harvest_plot = self.get_harvest_plot()
        domain_plot = self.get_domain_plot()
        return {
            'scripts': [domain_plot[0], harvest_plot[0]],
            'divs': [domain_plot[1], harvest_plot[1]],
        }

