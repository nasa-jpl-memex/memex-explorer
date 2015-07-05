#!/bin/bash
source activate memex_deploy
GIT_BRANCH='production' SECURITY_GROUP='memex-explorer-prod' HTPASSWD_PATH='XXX' AWS_ID='XXX' AWS_SECRET='XXX' python ec2-fabfile.py
