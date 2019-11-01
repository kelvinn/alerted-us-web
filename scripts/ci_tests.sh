#!/bin/sh

# Abort the script if any command fails
set -e

virtualenv .venv
source .venv/bin/activate
pip install -U docker-compose

docker-compose build
docker-compose down && docker-compose up -d

sleep 15 # Wait for DB to come up before proceeding. Can be better...

docker-compose run db /bin/sh -c 'exec psql -h db -U postgres -c "CREATE EXTENSION IF NOT EXISTS POSTGIS"'

docker-compose run web /bin/sh -c "python manage.py migrate --noinput"
docker-compose run web /bin/sh -c "python manage.py collectstatic --noinput"
docker-compose run web /bin/sh -c "coverage run manage.py test --parallel"
docker-compose stop && docker-compose rm -f
