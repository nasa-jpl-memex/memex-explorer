#  IMPORTS
# =========

# Standard Library
# ----------------

import os
from subprocess import Popen, PIPE
import shlex
from datetime import datetime

from abc import ABCMeta, abstractmethod, abstractproperty

# Local Imports
# -------------

from .config import SEED_FILES, MODEL_FILES, CONFIG_FILES, CRAWLS_PATH, LANG_DETECT_PATH, IMAGE_SPACE_PATH
from .db_api import get_data_source
from .utils import make_dir, make_dirs, run_proc


#  EXCEPTIONS
# ============

class CrawlException(Exception):
    pass

class NutchException(CrawlException):
    pass

class AcheException(CrawlException):
    pass


#  CLASSES
# ==========

class Crawl(object):
    """Abstract base class for crawls. This class encapsulates a few basic attributes:

        start_time (datetime.datetime)
        stop_time (datetime.datetime): (`None` if not yet stopped.)

        proc (int): Process ID of the crawl instance.

    @property
        duration (datetime.timedelta): The time elapsed
            between `start_time` and `stop_time` (if stopped) else
            between `start_time` and `datetime.now()`.


    Classes that inherit from `Crawl` are expected to implement the following:

    
    """

    __metaclass__ = ABCMeta

    def __init__(self, crawl_name, project_id):
        """Initialize common crawl attributes."""

        self.crawl_name = crawl_name
        self.project_id = project_id
        self.status = "Starting"

        # Handle to crawl process
        self.proc = None

    def start(self):
        subprocess.Popen(['mkdir', self.crawl_dir]).wait()
        with open(os.path.join(self.crawl_dir, 'stdout.txt'), 'w') as stdout:
            with open(os.path.join(self.crawl_dir,'stderr.txt'), 'w') as stderr:
                self.proc = subprocess.Popen(['ache', 'startCrawl', self.crawl_dir, self.config, self.seeds_file,
                                          self.model_dir, LANG_DETECT_PATH], stdout=stdout, stderr=stderr)
        return self.proc.pid
        # Common statistics to record across crawls, with suitable defaults
        self.start_time = datetime.now()
        self.stop_time = None


    @property
    def duration(self):
        if self.stop_time:
            delta = self.stop_time - self.start_time
        else:
            delta = datetime.now() - self.start_time
        return delta.total_seconds()


    @abstractmethod
    def statistics(self):
        return


    def get_status(self):
        self.proc.poll()
        if self.proc is None:
            self.status = "No process exists"
        elif self.proc.returncode is None:
            self.status = "Running crawl"
        elif self.proc.returncode < 0:
            self.status = "Crawl process was terminated by signal %s" % self.proc.returncode
        else:
            self.status = "Crawl process ended"
        return self.status

    def stop(self):
        if self.proc is not None:
            print("Killing %s" % str(self.proc.pid))
            self.proc.kill()
            self.stop_time = datetime.now()


class AcheCrawl(Crawl):

    def __init__(self, crawl_name, seeds_file, model_name, conf_name, project_id):
        self.config = os.path.join(CONFIG_FILES, conf_name)
        self.seeds_file = os.path.join(SEED_FILES, seeds_file)
        self.model_dir = os.path.join(MODEL_FILES, model_name)
        self.crawl_dir = os.path.join(CRAWLS_PATH, crawl_name)
        super(AcheCrawl, self).__init__(crawl_name, project_id)

    def start(self):
        with open(os.path.join(self.crawl_dir, 'stdout.txt'), 'w') as stdout:
            with open(os.path.join(self.crawl_dir,'stderr.txt'), 'w') as stderr:
                self.proc = run_proc("ache startCrawl {} {} {} {} {}".format(
                                 self.crawl_dir, self.config, self.seeds_file,
                                 self.model_dir, LANG_DETECT_PATH),
                            stdout=stdout, stderr=stderr)
        return self.proc.pid


    def statistics(self):
        harvest_source = get_data_source(self.project_id, self.crawl_name + "-harvest")
        harvest_path = CRAWLS_PATH + harvest_source.data_uri
        proc = run_proc("tail -n 1 %s" % harvest_path)
        stdout, stderr = proc.communicate()
        if stderr:
            raise AcheException(stderr)

        # from ipsh import ipsh
        # ipsh()

        ret = {}
        ret['nutch'] = False
        relevant, crawled = tuple(stdout.split('\t')[:2])
        ret['harvest_rate'] = "%.2f" % (float(relevant) / float(crawled))

        return ret

class NutchCrawl(Crawl):

    def __init__(self, seed_dir, crawl_dir, project_id, crawl_name, num_rounds=1):
        self.seed_dir =  os.path.join(SEED_FILES, seed_dir)
        self.crawl_dir = os.path.join(CRAWLS_PATH, crawl_dir)
        self.img_dir = os.path.join(IMAGE_SPACE_PATH, crawl_dir, 'images')
        #TODO Switch from `1` to parameter.
        self.number_of_rounds = num_rounds
        super(NutchCrawl, self).__init__(crawl_name, project_id)

    def start(self):
        make_dir(self.crawl_dir)
        self.proc = Popen(['crawl', self.seed_dir, self.crawl_dir, str(self.number_of_rounds)])
        return self.proc.pid


    def dump_images(self):
        make_dirs(self.img_dir)
        img_dump_proc = run_proc(
            "nutch dump -outputDir {} -segment {} -mimetype image/jpeg image/png".format(
                            self.img_dir, os.path.join(self.crawl_dir, 'segments')),
                        stdout=PIPE, stderr=PIPE)

        stdout, stderr = img_dump_proc.communicate()
        if stderr:
            raise NutchException(stderr)

        return "Dumping images"


    def statistics(self):
        crawl_db_dir = os.path.join(self.crawl_dir, 'crawldb')
        proc_str = "nutch readdb {} -stats".format(crawl_db_dir)
        stats_proc = run_proc(proc_str)
                                              
        stdout, stderr = stats_proc.communicate()
        if stderr:
            raise NutchException(stderr)

        ret = {}

        for line in stdout.split('\n'):
            if 'db_fetched' in line:
                ret['num_crawled'] = int(line.split('\t')[-1])

        # ret['duration'] = self.duration
        ret['nutch'] = True

        return ret