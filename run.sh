#!/bin/sh

python manage.py migrate --noinput
python manage.py collectstatic --noinput
uwsgi_python27 --enable-threads --single-interpreter --http-socket :8000 --module project.wsgi