#!/bin/bash

# Abort the script if any command fails
set -e

# Call this like deploy.sh some-name-on-docker-cloud https://some-name.com

TARGET_HOST=$1
SERVICE_NAME=$2

virtualenv ~/venv
source ~/venv/bin/activate

dig +short myip.opendns.com @resolver1.opendns.com

pip install fabric

fab -H root@$TARGET_HOST deploy:version=1.1.$SEMAPHORE_BUILD_NUMBER,service_name=$SERVICE_NAME