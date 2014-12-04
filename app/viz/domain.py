"""
Generate the domain plot.
"""
from __future__ import division
import csv
import sys
from blaze import *
import pandas as pd
from bokeh.plotting import *
from bokeh.objects import HoverTool
from bokeh.models import ColumnDataSource, DataRange1d, FactorRange
from collections import OrderedDict
import numpy as np
import datetime as dt
from bokeh.embed import components
from bokeh.resources import CDN
from tld import get_tld
from functools import partial

from plot import PlotManager


class Domain(PlotManager):

    # def __init__(self, crawled='crawledpages.csv', relevant='relevantpages.csv',
    #                    frontier='frontierpages.csv', output_dir='data_preprocessed'):
    def __init__(self, datasources, plot, sort='relevant'):

        self.crawled_data = datasources['crawled'].data_uri
        self.relevant_data = datasources['relevant'].data_uri
        self.frontier_data = datasources['frontier'].data_uri

        self.sort = sort

        super(Domain, self).__init__(plot)


    def update_source(self):

        # Relevant
        df = pd.read_csv(self.relevant_data, delimiter='\t', header=None, names=['url', 'timestamp'])
        df['domain'] = df['url'].apply(partial(get_tld, fail_silently=True))
        df1 = df.groupby(['domain']).size()

        # Crawled
        df = pd.read_csv(self.crawled_data, delimiter='\t', header=None, names=['url', 'timestamp'])
        df['domain'] = df['url'].apply(partial(get_tld, fail_silently=True))
        df2 = df.groupby(['domain']).size()

        # Frontier
        df = pd.read_csv(self.frontier_data, delimiter='\t', header=None, names=['url'])
        df['domain'] = df['url'].apply(partial(get_tld, fail_silently=True))
        df3 = df.groupby(['domain']).size()

        df = pd.concat((df1, df2, df3), axis=1)
        df.columns = ['relevant', 'crawled', 'frontier']

        # df = df.sort('relevant', ascending=False).head(25)
        df = df.sort(self.sort, ascending=False).head(25)

        for col in df.columns:
            df['%s_half' % col] = df[col] / 2

        df.reset_index(inplace=True)
        # print df

        source = into(ColumnDataSource, df)
        print source.data.values()
        return source


    def create_and_store(self):

        self.source = self.update_source()
        output_server(self.doc_name)
        curdoc().autostore = False

        p = figure(plot_width=400, plot_height=400,
            title="Domains Sorted by %s" % self.sort,
            x_range = DataRange1d(sources=[self.source.columns("crawled")]),
            y_range = FactorRange(factors=self.source.data['index']),
            tools='reset, resize, save')

        p.rect(y='index', x='crawled_half', height=0.75, width='crawled',
               color="red", fill_color="red", source = self.source, legend="crawled")
        p.rect(y='index', x='relevant_half', height=0.75, width='relevant',
               color="blue", fill_color="blue", source = self.source, legend="relevant")

        p.axis.major_label_text_font_size = "8pt"

        cursession().store_document(curdoc())
        
        autoload_tag = autoload_server(p, cursession())
        # Save ColumnDataSource model id to database model 
        self.plot.source_id = self.source._id

        # Save autoload_server tag as well
        self.plot.autoload_tag = autoload_tag
        db.session.flush()
        db.session.commit()
        return autoload_server(p, cursession())
