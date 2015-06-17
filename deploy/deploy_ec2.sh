#!/bin/bash
source activate memex_deploy
GIT_BRANCH='production' HTPASSWD_PATH='XXX' AWS_ID='XXX' AWS_SECRET='XXX' python ec2-fabfile.py
