#!/bin/sh

virtualenv ~/venv
source ~/venv/bin/activate

pip install -U docker-cloud requests==2.7.0
docker-cloud service set --image zephell/alerted-us-web:$SNAP_COMMIT_SHORT-$SNAP_PIPELINE_COUNTER $TUTUM_ENVIRONMENT_NAME --sync
docker-cloud service redeploy $TUTUM_ENVIRONMENT_NAME --sync && sleep 10
python tests/smoke.py $DEPLOYED_HOSTNAME