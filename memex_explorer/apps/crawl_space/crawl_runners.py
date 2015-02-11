"""Provides CrawlRunner subclasses to wrap crawl process execution and
monitoring.

"""

import os
import subprocess
import time

from abc import ABCMeta, abstractmethod #, abstractproperty


from apps.crawl_space.settings import (LANG_DETECT_PATH, CRAWL_PATH,
                                       MODEL_PATH, CONFIG_PATH)
from apps.crawl_space.utils import join, touch, rm_if_exists


# Exceptions
class CrawlException(Exception):
    pass

class NutchException(CrawlException):
    pass

class AcheException(CrawlException):
    pass



#  CLASSES
# ==========

class CrawlRunner(metaclass=ABCMeta):
    """Abstract base class for crawl runners.

    CrawlRunner subclasses are expected to implement these methods:
        run(self)
        log_statistics(self)

    Parameters
    ----------

    crawl_model : crawl_space.models.Crawl subclass

    Attributes
    ----------

    crawl_model : crawl_space.models.Crawl subclass
    crawl_dir : str
        Path to crawl directory,
          ex. `resources/crawls/4`.
    seeds_path : str
        Path to seeds file (or directory, in the case of Nutch),
          ex. `resources/crawls/4/seeds`.
    call : list(str)
        The tokenized call to the appropriate crawl process.

    """

    def __init__(self, crawl_model):
        """Initialize common CrawlRunner attributes based on `crawl_model`."""

        self.crawl_model = crawl_model
        self.crawl_dir = crawl_model.get_crawl_path()
        self.seeds_path = crawl_model.seeds_list.path
        self.stop_file = join(self.crawl_dir, 'stop')

    @property
    @abstractmethod
    def call(self):
        pass

    @abstractmethod
    def run(self):
        """Run the crawl.

        Note
        ----
        This method should be called via super() from a subclass.

        Operation
        ---------
        First, remove the stop file if it exists. This is a convenient action
        while developing, however, #TODO should raise an error if the stop
        file exists for a crawl that has not yet run.

        Second, open a subprocess based on `self.call` (defined by a subclass)
        and direct its output to an appropriate log file. Update the status.

        Then, as long as the process is running, every five seconds:
          1. Log statistics
          2. Check if a stop file has appeared, exit the process accordingly
        """

        rm_if_exists(self.stop_file)

        with open(join(self.crawl_dir, 'crawl_proc.log'), 'a') as stdout:
            self.proc = subprocess.Popen(call,
                stdout=stdout, stderr=subprocess.STDOUT)

        self.crawl_model.status = "running"
        self.crawl_model.save()

        stopped = False
        while self.proc.poll() is None:
            self.log_statistics()
            if rm_if_exists(self.stop_file):
                stopped = True
                break

            print('.', end="", flush=True)
            time.sleep(5)

        if not stopped:
            self.proc.terminate()
            #TODO kill nutch child processes

        self.crawl.status = "stopped"
        self.crawl.save()
        return True

    @abstractmethod
    def log_statistics(self):
        pass


class AcheCrawlRunner(CrawlRunner):

    def __init__(self, crawl_model):
        """ACHE specific attributes."""

        super().__init__(crawl_model)

        self.config_dir = join(CONFIG_PATH, self.crawl_model.config)
        self.model_dir = self.crawl_model.get_model_path()

        self.call = ["ache", "startCrawl",
                     self.crawl_dir,
                     self.config_dir,
                     self.seeds_path,
                     self.model_dir,
                     LANG_DETECT_PATH]


    def run(self):
        """Implemented in CrawlRunner."""
        super().run()


    def log_statistics(self):
        harvest_path = join(self.crawl_dir, 'data_monitor/harvestinfo.csv')
        proc = subprocess.Popen(["tail", "-n", "1", harvest_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        if stderr and b"No such file or directory" not in stderr:
                raise AcheException(stderr)

        harvest_stats = stdout.decode() 

        if not harvest_stats:
            return

        relevant, crawled = tuple(harvest_stats.split('\t')[:2])
        self.crawl.harvest_rate = "%.2f" % (float(relevant) / float(crawled))
        self.crawl.pages_crawled = crawled
        self.crawl.save()



class NutchCrawl(CrawlRunner):

    def __init__(self, crawl):
        """Nutch specific attributes."""

        super().__init__(crawl)


        self.call = ["crawl",
                     self.seed_dir,
                     self.crawl_dir,
                     "1"]

    def run(self):
        rm_if_exists(stop_file)


        with open(join(self.crawl_dir, 'nutch.log'), 'a') as stdout:
            self.proc = subprocess.Popen(call,
                stdout=stdout, stderr=subprocess.STDOUT)

        self.crawl.status = "running"
        self.crawl.save()

        while self.proc.poll() is None:
            self.log_statistics()
            if rm_if_exists(self.stop_file):
                break

            print('.', end="", flush=True)
            time.sleep(5)

        self.proc.terminate()
        self.crawl.status = "stopped"
        self.crawl.save()
        return True



    def log_statistics(self):
        pass
        # TODO


    def dump_images(self, image_space):
        pass
