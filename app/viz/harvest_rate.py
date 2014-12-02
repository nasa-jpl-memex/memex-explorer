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
from bokeh.embed import components
from bokeh.resources import CDN

from harvest import Harvest

class HarvestRate(Harvest):

    def __init__(self, datasource, plot):
        # plot attributes: name description plot
        # data attributes: name data_uri description plots 
        self.harvest_data = data.data_uri
        super(HarvestRate, self).__init__(plot)

    def update_source(self):
        super(HarvestRate, self).update_source(plot)


    def create_and_store(self):

        self.source = self.update_source()

        output_server(self.doc_name)
        curdoc().autostore = False

        p = figure(plot_width=500, plot_height=250,
               title="Harvest Rate", x_axis_type='datetime',
               tools='pan, wheel_zoom, box_zoom, reset, resize, save, hover')

        p.line(x="timestamp", y="harvest_rate", fill_alpha=0.6, color="blue", width=0.2, legend="harvest_rate", source=self.source)
        p.scatter(x="timestamp", y="harvest_rate", alpha=0, color="blue", legend="harvest_rate", source=self.source)

        hover = curplot().select(dict(type=HoverTool))
        hover.tooltips = OrderedDict([
            ("harvest_rate", "@harvest_rate"),
        ])

        p.legend.orientation = "top_left"
        
        cursession().store_document(curdoc())
        return autoload_server(p, cursession())
