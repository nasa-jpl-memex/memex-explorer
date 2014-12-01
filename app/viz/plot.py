from abc import ABCMeta, abstractmethod

class Plot(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def update_source(self):
        pass

    @abstractmethod
    def create_and_store(self):
        pass

    @abstractmethod
    def push_to_server(self):
        pass
