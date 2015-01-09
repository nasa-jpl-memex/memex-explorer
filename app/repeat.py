
print "W$TWFD"

import os
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

def keep_going(crawl_dir=args.crawl_dir, crawl_id=args.crawl_id):
    return True
    # return os.path.exists(os.path.join(crawl_dir, str(crawl_id), 'keep_going'))

counter = 1

while keep_going():
    print "Loop %d" % counter
    print
    print
    counter += 1
    proc = subprocess.Popen(shlex.split("crawl {} {} 1".format(args.seed_dir, args.crawl_dir)))
    stdout, stderr = proc.communicate()
    if stderr:
        raise NutchException(stderr)

    print stdout

print "Finished"
