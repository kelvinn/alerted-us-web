#!/bin/bash

# Abort the script if any command fails
set -e

# Create a virtual environment
python -m venv .venv && source .venv/bin/activate

# Install docker-compose
python -m pip install -U docker-compose

# Build and start things up
docker-compose build
docker-compose down && docker-compose up -d

# Wait for DB to come up before proceeding. Can be better...
sleep 15

# Run the tests
docker-compose run db /bin/sh -c 'exec psql -h db -U postgres -c "CREATE EXTENSION IF NOT EXISTS POSTGIS"'
docker-compose run web /bin/sh -c "python manage.py migrate --noinput"
docker-compose run web /bin/sh -c "python manage.py collectstatic --noinput"
docker-compose run web /bin/sh -c "coverage run manage.py test --parallel"
docker-compose stop && docker-compose rm -f
