#!/bin/sh

python manage.py migrate --noinput
python manage.py collectstatic --noinput
ln -s /usr/lib/python2.7/plat-*/_sysconfigdata_nd.py /usr/lib/python2.7/

# --enable-threads --single-interpreter is needed for NewRelic
uwsgi --enable-threads --single-interpreter --vacuum --http :8000 --module project.wsgi
