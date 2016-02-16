#!/bin/sh

python manage.py migrate --noinput
python manage.py collectstatic --noinput
ln -s /usr/lib/python2.7/plat-*/_sysconfigdata_nd.py /usr/lib/python2.7/
uwsgi --master --processes=5 --harakiri=20 --max-requests=5000 --vacuum --http :8000 --module project.wsgi
