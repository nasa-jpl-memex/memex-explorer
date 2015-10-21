from StringIO import StringIO

import pandas as pd

from harvest import Harvest
from domain import Domain


class PlotsNotReadyException(Exception):
    pass


class AcheDashboard(object):

    def __init__(self, crawl):
        self.crawl = crawl
        if self.crawl.crawler != "ache":
            raise ValueError("Crawl must be using the Ache crawler.")
        self.harvest = Harvest(crawl)
        self.domain = Domain(crawl)

    def get_harvest_plot(self):
        # TODO: Remove Pokemon exception catching
        try:
            script, div = self.harvest.create()
        except:
            return [None, None]
        return [script, div]

    def get_domain_plot(self):
        # TODO: Remove Pokemon exception catching
        try:
            script, div = self.domain.create()
        except Exception:
            return [None, None]
        return [script, div]

    def get_relevant_seeds(self):
        # Converts stdout to StringIO to allow pandas to read it as a file
        seeds = pd.read_csv(StringIO(self.domain.get_relevant_data()),
                           delimiter='\t', header=None,
                           names=['url', 'timestamp'])
        return seeds['url'].to_dict().values()

    def get_plots(self):
        harvest_plot = self.get_harvest_plot()
        domain_plot = self.get_domain_plot()
        return {
            'scripts': [domain_plot[0], harvest_plot[0]],
            'divs': [domain_plot[1], harvest_plot[1]],
        }

