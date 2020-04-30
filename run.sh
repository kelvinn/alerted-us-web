#!/bin/sh

echo "Performing database migrations..."

python manage.py migrate --noinput

echo "Collecting static files..."

python manage.py collectstatic --noinput

echo "Printing Django version"

python manage.py --version

echo "Starting Gunicorn..."

#uwsgi --http-socket :8000 --wsgi-file project/wsgi.py --master --processes 2 --threads 2
#uwsgi --enable-threads --single-interpreter --plugins python --vacuum --http-socket :8000 --module project.wsgi

[ -z "$PORT" ] && export PORT=8000;

#uwsgi --socket 0.0.0.0:$PORT --protocol=http -w project.wsgi:application

gunicorn project.wsgi:application --bind 0.0.0.0:$PORT --max-requests 5000 --workers 2

