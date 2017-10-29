#!/bin/sh

echo "Performing database migrations..."

python manage.py migrate --noinput

echo "Collecting static files..."

python manage.py collectstatic --noinput

echo "Creating symlink as needed..."

ln -s /usr/lib/python2.7/plat-*/_sysconfigdata_nd.py /usr/lib/python2.7/

echo "Starting uWSGI server..."

#gunicorn project.wsgi:application --bind 0.0.0.0:8000 --max-requests 500 --workers 2

#uwsgi --http-socket :8000 --wsgi-file project/wsgi.py --master --processes 2 --threads 2
#uwsgi --enable-threads --single-interpreter --plugins python --vacuum --http-socket :8000 --module project.wsgi


uwsgi --socket 0.0.0.0:8000 --protocol=http -w project.wsgi:application