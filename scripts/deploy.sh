#!/bin/bash

# Abort the script if any command fails
set -e

# Call this like deploy.sh some-name-on-docker-cloud https://some-name.com

OS_USER=$1

ssh-keyscan -H -p 22 production-alerted.rhcloud.com >> ~/.ssh/known_hosts
git remote set-url production "ssh://$OS_USER@production-alerted.rhcloud.com/~/git/production.git/"
git push --force production master
pip install requests
python tests/smoke.py https://alerted.us

# Deploy should have succeeded now, so posting release

export REVISION=`git log -n 1 --pretty="format:%H"`
export BRANCH=`git rev-parse --abbrev-ref HEAD`
export URL=https://intake.opbeat.com/api/v1/organizations/$ORGANIZATION_ID/apps/$APP_ID/releases/
curl $URL -H "Authorization: Bearer $SECRET_TOKEN" -d rev=$REVISION -d branch=$BRANCH -d status=completed