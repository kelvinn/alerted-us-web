python manage.py migrate --noinput
python manage.py collectstatic --noinput
uwsgi --http :8000 --module project.wsgi
