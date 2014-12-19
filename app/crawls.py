import subprocess
import os

from .config import SEED_FILES, MODEL_FILES, CONFIG_FILES, CRAWLS_PATH, LANG_DETECT_PATH


class AcheCrawl(object):

    def __init__(self, crawl_name, seeds_file, model_name, conf_name):
        self.crawl_name = crawl_name
        self.config = os.path.join(CONFIG_FILES, conf_name)
        self.seeds_file = os.path.join(SEED_FILES, seeds_file)
        self.model_dir = os.path.join(MODEL_FILES, model_name)
        self.crawl_dir = os.path.join(CRAWLS_PATH, crawl_name)
        self.proc = None

    def start(self):
        with open('stdout.txt', 'w') as f:
            self.proc = subprocess.Popen(['ache', 'startCrawl', self.crawl_dir, self.config, self.seeds_file,
                                          self.model_dir, LANG_DETECT_PATH], stdout=f)
        return self.proc.pid

    def stop(self):
        if self.proc is not None:
            print("Killing %s" % str(self.proc.pid))
            self.proc.kill()

    def status(self):
        if self.proc is None:
            return "No process exists"
        elif self.proc.returncode is None:
            return "Running"
        elif self.proc.returncode < 0:
            return "Stopped (Unused)"
        else:
            return "An error occurred"


class NutchCrawl(object):

    def __init__(self, seed_dir, crawl_dir):
        self.seed_dir =  SEED_FILES + "/" + seed_dir
        self.crawl_dir = CRAWLS_PATH + "/" + crawl_dir
        #TODO Switch from "2" to parameter.
        # For now let's set up number_of_rounds to 2.
        self.number_of_rounds = "2"
        #self.number_of_rounds = numberOfRounds
        self.proc = None
        self.create_dir = subprocess.Popen(['mkdir', self.crawl_dir])

    def start(self):
        self.proc = subprocess.Popen(['crawl', self.seed_dir, self.crawl_dir, self.number_of_rounds])
        return self.proc.pid

    def stop(self):
        if self.proc is not None:
            print("Killing %s" % str(self.proc.pid))
            self.proc.kill()

    def status(self):
        if self.proc is None:
            return "No process exists"
        elif self.proc.returncode is None:
            return "Running"
        elif self.proc.returncode < 0:
            return "Stopped (Unused)"
        else:
            return "An error occurred"
