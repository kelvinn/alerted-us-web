#!/bin/bash

python manage.py migrate --noinput
python manage.py collectstatic --noinput
uwsgi --enable-threads --single-interpreter --http :8000 --module project.wsgi