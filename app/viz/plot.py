from abc import ABCMeta, abstractmethod
from bokeh.models import ColumnDataSource
from bokeh.plotting import Document, Session


class PlotManager(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, plot):
        self.doc_name = '%d_%s' % (plot.id, plot.name)
        self.plot = plot

    @abstractmethod
    def update_source(self):
        pass

    @abstractmethod
    def create_and_store(self):
        pass

    def push_to_server(self):
        # Refresh data; self.source should be a ColumnDataSource instance
        self.source = self.update_source()
        s = Session()

        # Set docid; seems to be required for `s.pull()`
        s.docid = s.find_doc(self.doc_name)
        doc = Document()
        json_source = s.pull(typename="ColumnDataSource", objid=self.plot.source_id)[0]
        doc.load(json_source)
        cds = [x for x in doc._models.values() if isinstance(x, ColumnDataSource)][0]

        # Attach new data and push
        cds.data = self.source.data
        s.store_objects(cds)


def plot_exists(plot_model):
    s = Session()
    doc_name = '%d_%s' % (plot_model.id, plot_model.name)
    return any(x['title'] == doc_name for x in s.userinfo['docs'])
