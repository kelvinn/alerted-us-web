#!/bin/sh

# Call this like deploy.sh some-name-on-docker-cloud https://some-name.com

virtualenv ~/venv
source ~/venv/bin/activate

TARGET_ENVNAME=$1
TARGET_HOSTNAME=$2

pip install -U docker-cloud requests==2.7.0
docker-cloud service set --image zephell/alerted-us-web:$SEMAPHORE_BUILD_NUMBER-$SEMAPHORE_BRANCH_ID  --sync
docker-cloud service set --image zephell/alerted-us-web:$SNAP_COMMIT_SHORT-$SNAP_PIPELINE_COUNTER $TARGET_ENVNAME --sync
docker-cloud service redeploy $TARGET_ENVNAME --sync && sleep 10
python tests/smoke.py $TARGET_HOSTNAME