import os
import subprocess
import shlex
import errno


def run_proc(process_str, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
    return subprocess.Popen(shlex.split(process_str),
                            stdout=stdout, stderr=stderr)


def make_dir(directory):
    try:
        os.mkdir(directory)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(directory):
            pass
        else:
            raise


def make_dirs(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
