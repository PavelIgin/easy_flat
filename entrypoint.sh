python3 manage.py migrate
python3 manage.py collectstatic
gunicorn easy_flat.wsgi:application --bind 0.0.0.0:8000
