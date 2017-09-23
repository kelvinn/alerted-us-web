#!/bin/sh

echo "Performing database migrations..."

python manage.py migrate --noinput

echo "Collecting static files..."

python manage.py collectstatic --noinput

echo "Creating symlink as needed..."

ln -s /usr/lib/python2.7/plat-*/_sysconfigdata_nd.py /usr/lib/python2.7/

echo "Starting uWSGI server..."

gunicorn project.wsgi:application --bind 0.0.0.0:8000 --workers 3
