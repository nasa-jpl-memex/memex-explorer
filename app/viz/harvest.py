from __future__ import division
import csv
import sys
from blaze import *
import pandas as pd
from bokeh.plotting import *
from bokeh.objects import HoverTool
from collections import OrderedDict
import numpy as np
import datetime as dt

def generate_harvest():
    """
    Generates a fake_harvest_data
    """
    harvest_data = 'data_monitor/harvestinfo.csv'
    return harvest_data


class Harvest(object):

    def __init__(self, input_data='data_monitor/harvestinfo.csv'):
        self.harvest_data = input_data
        self.source = self.update_source()
        self.plot, self.rate_plot = self.create_plot()

    def update_source(self):
        t = Table(CSV(self.harvest_data, columns=['relevant_pages', 'downloaded_pages', 'timestamp']))
        t = transform(t, timestamp=t.timestamp.map(dt.datetime.fromtimestamp, schema='{timestamp: datetime}'))
        t = transform(t, date=t.timestamp.map(lambda x: x.date(), schema='{date: date}'))
        t = transform(t, harvest_rate=t.relevant_pages/t.downloaded_pages)

        source = into(ColumnDataSource, t)

        return source

    def create_plot(self, output_html='harvest.html'):

        output_file(output_html)

        figure(plot_width=500, plot_height=250, title="Harvest Plot", tools='pan, wheel_zoom, box_zoom, reset, resize, save, hover', x_axis_type='datetime')
        hold()

        scatter(x="timestamp", y="relevant_pages", fill_alpha=0.6, color="red", source=self.source)
        line(x="timestamp", y="relevant_pages", color="red", width=0.2, legend="relevant", source=self.source)
        scatter(x="timestamp", y="downloaded_pages", fill_alpha=0.6, color="blue", source=self.source)
        line(x="timestamp", y="downloaded_pages", color="blue", width=0.2, legend="downloaded", source=self.source)

        hover = curplot().select(dict(type=HoverTool))
        hover.tooltips = OrderedDict([
            ("harvest_rate", "@harvest_rate"),
        ])

        legend().orientation = "top_left"

        harvest_plot = curplot()

        figure(plot_width=500, plot_height=250, title="Harvest Rate", x_axis_type='datetime', tools='pan, wheel_zoom, box_zoom, reset, resize, save, hover')
        line(x="timestamp", y="harvest_rate", fill_alpha=0.6, color="blue", width=0.2, legend="harvest_rate", source=self.source)
        scatter(x="timestamp", y="harvest_rate", alpha=0, color="blue", legend="harvest_rate", source=self.source)

        hover = curplot().select(dict(type=HoverTool))
        hover.tooltips = OrderedDict([
            ("harvest_rate", "@harvest_rate"),
        ])

        harvest_rate_plot = curplot()

        return harvest_plot, harvest_rate_plot
