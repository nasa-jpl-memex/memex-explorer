from abc import ABCMeta, abstractmethod
from bokeh.models import ColumnDataSource
from bokeh.plotting import Document, Session

from harvest import Harvest
from domain import Domain

class AchePlots(object):

    def __init__(self, crawl):
        self.harvest = Harvest(crawl)
        self.domain = Domain(crawl)

    def get_harvest_plot(self):
        script, div = self.harvest.create()
        return [script, div]

    def get_domain_plot(self):
        script, div = self.domain.create()
        return [script, div]

    def get_plots(self):
        harvest_plot = self.get_harvest_plot()
        domain_plot = self.get_domain_plot()
        return {
            'scripts': [harvest_plot[0], domain_plot[0]],
            'divs': [harvest_plot[1], domain_plot[1]],
        }

