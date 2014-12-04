from __future__ import division
import pandas as pd
import numpy as np

from blaze import *
from bokeh.plotting import *
from bokeh.models import ColumnDataSource
from functools import partial

from plot import PlotManager


class Termite(PlotManager):
    """Create a termite plot to visualize topics and words from an LDA.
       See <http://vis.stanford.edu/papers/termite>"""


    def __init__(self, datasource, plot):
        self.termite_data = datasource.data_uri
        super(Termite, self).__init__(plot)

    def preprocess_file(self):
        """Transform the summary.txt file into two CSV files with
        the specified formatting."""

        return
        # df = pd.read_csv(self.termite_data, delimiter='\t', header=None,
        #                  names=["topic", "keyword", "value"],
        #                  usecols=["topic", "value"])
        # df.dropna(subset=['topic'], inplace=True)
        # df.to_csv('topics_data.csv', index=False)


        # df = pd.read_csv(self.termite_data, delimiter='\t', header=None,
        #                  names=["topic", "keyword", "value"])
        # df.topic.fillna(method='ffill', inplace=True)
        # df.set_index('topic', drop=True, inplace=True)
        # df.dropna(inplace=True)
        # df.to_csv('termite_data.csv')

    @staticmethod
    def size(x, MIN, MAX):
        """Return a scaled pixel size suitable for display."""
        return np.sqrt((x - MIN)/(MAX - MIN)) * 50

    def update_source(self):

        df = pd.read_csv(self.termite_data, delimiter='\t', header=None,
                         names=["topic", "keyword", "value"])
        df.topic.fillna(method='ffill', inplace=True)
        df.dropna(subset=['keyword'], inplace=True)
        df.sort('value', ascending=False, inplace=True)

        MAX = df.value.max()
        MIN = df.value.min()
        
        df['size'] = df.value.apply(partial(self.size, MIN, MAX))

        self.WORDS = list(df['keyword'].unique())
        self.TOPICS = list(df['topic'].unique())

        source = into(ColumnDataSource, df)
        return source

    def create_and_store(self):

        self.source = self.update_source()

        output_server(self.doc_name)
        curdoc().autostore = False

        p = figure(x_range=self.TOPICS, y_range=self.WORDS, 
               plot_width=1000, plot_height=1700,
               title="Termite Plot", tools='resize, save')

        p.circle(x="topic", y="keyword", size="size", fill_alpha=0.6, source=self.source)
        p.xaxis.major_label_orientation = np.pi/3

        # Save ColumnDataSource model id to database model 
        self.plot.source_id = self.source._id
        db.session.flush()
        db.session.commit()

        cursession().store_document(curdoc())
        return autoload_server(p, cursession())
