#!/bin/sh

pip install -U tutum requests==2.7.0 loaderio
tutum service set --image zephell/alerted-us-web:$SNAP_COMMIT_SHORT-$SNAP_PIPELINE_COUNTER $TUTUM_ENVIRONMENT_NAME --sync
tutum service redeploy $TUTUM_ENVIRONMENT_NAME --sync && sleep 10
python tests/smoke.py $DEPLOYED_HOSTNAME