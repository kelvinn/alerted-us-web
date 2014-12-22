python manage.py migrate --noinput
python manage.py collectstatic --noinput
supervisord -n
