#!/bin/bash

# Abort the script if any command fails
set -e

python -m venv .venv && source .venv/bin/activate

pip install -U docker-compose

docker-compose up -d

sleep 15 # Wait for DB to come up before proceeding. Can be better...

docker-compose run db sh -c 'exec psql -h db -U postgres -c "CREATE EXTENSION IF NOT EXISTS POSTGIS"'

docker-compose run web bash -c "python manage.py migrate --noinput"
docker-compose run web bash -c "python manage.py collectstatic --noinput"
docker-compose run web bash -c "python manage.py test --parallel"
docker-compose stop && docker-compose rm -f
