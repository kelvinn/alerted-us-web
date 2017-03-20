#!/bin/sh

# Abort the script if any command fails
set -e

docker login -e $DOCKER_EMAIL -u $DOCKER_USER -p $DOCKER_PASS
docker tag alertedusweb_web zephell/alerted-us-web:1.1.$SEMAPHORE_BUILD_NUMBER
docker push zephell/alerted-us-web:1.1.$SEMAPHORE_BUILD_NUMBER