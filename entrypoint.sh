python manage.py migrate
python manage.py collectstatic
gunicorn easy_flat.wsgi:application --bind 0.0.0.0:8000
