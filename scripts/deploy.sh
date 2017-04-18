#!/bin/bash

# Abort the script if any command fails
set -e

# Call this like deploy.sh some-name-on-docker-cloud https://some-name.com

OS_USER=$1

ssh-keyscan -H -p 22 production-alerted.rhcloud.com >> ~/.ssh/known_hosts
git remote add production "ssh://$OS_USER@production-alerted.rhcloud.com/~/git/production.git/"
git push --force production master
pip install requests
python tests/smoke.py https://alerted.us