from abc import ABCMeta, abstractmethod

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

    @abstractmethod
    def push_to_server(self):
        pass
