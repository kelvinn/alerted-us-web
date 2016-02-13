#!/bin/sh

pip install -U docker-compose==1.4.2


sudo docker-compose up -d
sudo docker-compose run db sh -c 'exec psql -h "$DB_PORT_5432_TCP_ADDR" -p "$DB_PORT_5432_TCP_PORT" -U postgres -c "CREATE EXTENSION IF NOT EXISTS POSTGIS"'
sudo docker-compose run web ./scripts/run_ci_tests.sh
sudo docker login -e $DOCKER_EMAIL -u $DOCKER_USER -p $DOCKER_PASS
sudo docker tag repo_web zephell/alerted-us-web:$SNAP_COMMIT_SHORT-$SNAP_PIPELINE_COUNTER
sudo docker push zephell/alerted-us-web:$SNAP_COMMIT_SHORT-$SNAP_PIPELINE_COUNTER