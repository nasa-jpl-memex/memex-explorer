from __future__ import division
import os
from blaze import into
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from collections import OrderedDict
from bokeh.embed import components
import subprocess
import shlex
from StringIO import StringIO


GREEN = "#47a838"
DARK_GRAY = "#2e2e2e"
LIGHT_GRAY = "#6e6e6e"


class Harvest(object):
    """Create a line plot to compare the growth of crawled and relevant pages in the crawl."""

    def __init__(self, crawl):
        self.source = None
        self.harvest_data = os.path.join(crawl.get_crawl_path(), 'data_monitor/harvestinfo.csv')

    def update_source(self):
        proc = subprocess.Popen(shlex.split("tail -n 800 %s" % self.harvest_data),
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stderr = proc.communicate()

        if stderr or not stdout:
            raise ValueError("harvestinfo.csv is empty")

        # Converts stdout to StringIO to allow pandas to read it as a file

        df = pd.read_csv(StringIO(stdout), delimiter='\t',
                         names=['relevant_pages', 'downloaded_pages', 'timestamp'])
        df['harvest_rate'] = df['relevant_pages'] / df['downloaded_pages']
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

        source = into(ColumnDataSource, df)
        return source

    def create(self):
        self.source = self.update_source()

        p = figure(plot_width=400, plot_height=400,
                   title="Harvest Plot", x_axis_type='datetime',
                   tools='pan, wheel_zoom, box_zoom, reset, resize, save, hover')

        p.line(x="timestamp", y="relevant_pages", color=GREEN, line_width=0.2,
               legend="relevant", source=self.source)
        p.scatter(x="timestamp", y="relevant_pages", fill_alpha=0.6,
                  color=GREEN, source=self.source)

        p.line(x="timestamp", y="downloaded_pages", color=DARK_GRAY, line_width=0.2,
               legend="downloaded", source=self.source)
        p.scatter(x="timestamp", y="downloaded_pages", fill_alpha=0.6,
                 color=DARK_GRAY, source=self.source)

        hover = p.select(dict(type=HoverTool))
        hover.tooltips = OrderedDict([
            ("harvest_rate", "@harvest_rate"),
        ])

        p.legend.orientation = "top_left"

        script, div = components(p)
        return (script, div)
