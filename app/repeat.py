
print "W$TWFD"

import argparse
import subprocess
import shlex

def parse_args():
    parser = argparse.ArgumentParser(description="Nutch Repeater")

    parser.add_argument("--crawl_id", type=int, required=True,
                        help="ID of crawl instance")
    parser.add_argument("--seed_dir", type=str, required=True,
                        help="Seed directory")
    parser.add_argument("--crawl_dir", type=str, required=True,
                        help="Crawl directory")

    return parser.parse_args()


print "woohoo!!"

args = parse_args()

def keep_going(args.crawl_dir, args.crawl_id):
    
return os.path.exists(os.path.join())
return crawl.status is not "stop requested"

while keep_going(args.crawl_id):
    proc = subprocess.Popen(shlex.split("crawl {} {} 1".format(args.seed_dir, args.crawl_dir)))
    stdout, stderr = proc.communicate()
    if stderr:
        raise NutchException(stderr)

    print stdout
