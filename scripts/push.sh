#!/bin/sh

# Abort the script if any command fails
set -e

docker login -e $DOCKER_EMAIL -u $DOCKER_USER -p $DOCKER_PASS
docker tag repo_web zephell/alerted-us-web:$SNAP_PIPELINE_COUNTER-$SNAP_COMMIT_SHORT
docker push zephell/alerted-us-web:$SNAP_PIPELINE_COUNTER-$SNAP_COMMIT_SHORT