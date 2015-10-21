"""
Generate a bar chart of number of pages crawled in each domain.
"""
from __future__ import division

import pandas as pd
import os
from blaze import into
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.models import ColumnDataSource, Range1d, FactorRange
from tld import get_tld
import traceback
import subprocess
import shlex
from StringIO import StringIO


GREEN = "#47a838"
DARK_GRAY = "#2e2e2e"
LIGHT_GRAY = "#6e6e6e"
TAIL_LENGTH = 10000


class Domain(object):

    def __init__(self, crawl, sort='crawled'):
        # TODO Retrieve plot datasources from db
        self.crawled_data = os.path.join(crawl.get_crawl_path(), 'data_monitor/crawledpages.csv')
        self.relevant_data = os.path.join(crawl.get_crawl_path(), 'data_monitor/relevantpages.csv')

        self.sort = sort

    def extract_tld(self, url):
        try:
            return get_tld(url)
        except:
            traceback.print_exc()
            print "\n\nInvalid url: %s" % url
            return url

    def update_source(self):
        df = pd.read_csv(StringIO(self.get_relevant_data()), delimiter='\t', header=None, names=['url', 'timestamp'])
        df['domain'] = df['url'].apply(self.extract_tld)
        df1 = df.groupby(['domain']).size()

        df = pd.read_csv(StringIO(self.get_crawled_data()), delimiter='\t', header=None, names=['url', 'timestamp'])
        df['domain'] = df['url'].apply(self.extract_tld)
        df2 = df.groupby(['domain']).size()

        df = pd.concat((df1, df2), axis=1)
        df.columns = ['relevant', 'crawled']

        df = df.sort(self.sort, ascending=False).head(25).fillna(value=0)

        for col in df.columns:
            df['%s_half' % col] = df[col] / 2

        df.reset_index(inplace=True)

        df.rename(columns={'index':'domain'}, inplace=True)

        source = into(ColumnDataSource, df)
        return source

    def get_crawled_data(self, tail_length=TAIL_LENGTH):
        crawled_proc = subprocess.Popen(shlex.split("tail -n %d %s" % (tail_length,
                                         self.crawled_data)),
                                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = crawled_proc.communicate()
        return stdout

    def get_relevant_data(self, tail_length=TAIL_LENGTH):
        relevant_proc = subprocess.Popen(shlex.split("tail -n %d %s" % (tail_length,
                                         self.relevant_data)),
                                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = relevant_proc.communicate()
        return stdout

    def create(self):
        self.source = self.update_source()

        max_data = max(max(self.source.data['relevant']), max(self.source.data['crawled']))
        xdr = Range1d(start=0, end=max_data)

        p = figure(plot_width=400, plot_height=400,
                   title="Domains Sorted by %s" % self.sort, x_range = xdr,
                   y_range = FactorRange(factors=self.source.data['domain']),
                   tools='reset, resize, save')

        p.rect(y='domain', x='crawled_half', width="crawled", height=0.75,
               color=DARK_GRAY, source =self.source, legend="crawled")
        p.rect(y='domain', x='relevant_half', width="relevant", height=0.75,
               color=GREEN, source =self.source, legend="relevant")

        p.ygrid.grid_line_color = None
        p.xgrid.grid_line_color = '#8592A0'
        p.axis.major_label_text_font_size = "8pt"

        script, div = components(p)

        if os.path.exists(self.crawled_data) and os.path.exists(self.relevant_data):
            return (script, div)
