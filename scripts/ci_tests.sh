#!/bin/sh

pip install -U docker-compose
sudo docker-compose up -d
sudo docker-compose run db sh -c 'exec psql -h "$DB_PORT_5432_TCP_ADDR" -p "$DB_PORT_5432_TCP_PORT" -U postgres -c "CREATE EXTENSION IF NOT EXISTS POSTGIS"'
sudo docker-compose run web ./run_ci_tests.sh
sudo docker login -e $TUTUM_EMAIL -u $TUTUM_USER -p $TUTUM_PASS tutum.co
sudo docker tag repo_web tutum.co/zephell/alerted-us-web:$SNAP_COMMIT_SHORT-$SNAP_PIPELINE_COUNTER
sudo docker push tutum.co/zephell/alerted-us-web:$SNAP_COMMIT_SHORT-$SNAP_PIPELINE_COUNTER