import subprocess
from .config import ACHE_PATH, SEED_FILES, MODEL_FILES, CONFIG_FILES, CRAWLS_PATH

class AcheCrawl(object):

    def __init__(self, crawl_name, seed_file, model_name, crawl_dir):
        self.crawl_name = crawl_name
        self.config = "conf/conf_default"
        #TODO Switch from default configuration to custom
        #self.config = CONFIG_FILES + "/" + conf_name
        self.seed_file = SEED_FILES + "/" + seed_file
        self.model_name = MODEL_FILES + "/" + model_name + "/"
        self.crawl_dir = CRAWLS_PATH + "/" + crawl_dir
        self.proc = None

    def start(self):
        self.proc = subprocess.Popen(['ache/run_ache_crawler.sh', ACHE_PATH, self.crawl_name, self.config,
                                      self.seed_file, self.model_name, self.crawl_dir])
        #self.proc = subprocess.Popen('./count_things.sh', shell=True)
        return self.proc.pid

    def stop(self):
        if self.proc is not None:
            print("Killing %s" % str(self.proc.pid))
            self.proc.kill()
            proc2 = subprocess.Popen(['ache/stop_ache_crawler.sh', ACHE_PATH, self.crawl_name])

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
        self.seed_dir = seed_dir
        self.crawl_dir = crawl_dir
        #TODO Switch from "2" to parameter.
        # For now let's set up number_of_rounds to 2.
        self.number_of_rounds = "2"
        #self.number_of_rounds = numberOfRounds
        self.proc = None

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
