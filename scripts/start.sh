#!/bin/sh

# Abort the script if any command fails
set -e

virtualenv ~/venv
source ~/venv/bin/activate
pip install -U docker-compose

docker-compose build
docker-compose start db

sleep 15 # Wait for DB to come up before proceeding. Can be better...

docker-compose run db sh -c 'exec psql -h db -U postgres -c "CREATE EXTENSION IF NOT EXISTS POSTGIS"'

docker-compose run web /bin/bash -c "python manage.py migrate --noinput"
docker-compose run web /bin/bash -c "python manage.py collectstatic --noinput"

