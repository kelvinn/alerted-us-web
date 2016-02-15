#!/bin/sh

virtualenv ~/venv
source ~/venv/bin/activate
pip install -U docker-compose==1.4.2

docker-compose up -d
docker-compose run db sh -c 'exec psql -h "$DB_PORT_5432_TCP_ADDR" -p "$DB_PORT_5432_TCP_PORT" -U postgres -c "CREATE EXTENSION IF NOT EXISTS POSTGIS"'
docker-compose run web /bin/bash -c "python manage.py migrate --noinput"
docker-compose run web /bin/bash -c "python manage.py collectstatic --noinput"
docker-compose run web /bin/bash -c "python manage.py test"
