#!/bin/sh

pip install -U tutum requests loaderio
tutum service set --image tutum.co/zephell/alerted-us-web:$SNAP_COMMIT_SHORT-$SNAP_PIPELINE_COUNTER $TUTUM_ENVIRONMENT_NAME --sync
tutum service redeploy $TUTUM_ENVIRONMENT_NAME --sync
python tests/smoke.py $DEPLOYED_HOSTNAME