#!/bin/bash
source activate memex-deploy
GIT_BRANCH='XXX' AWS_ID='AKIAJUKVMXICU4WHXMIA' AWS_SECRET='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' python ec2-deploy.py
