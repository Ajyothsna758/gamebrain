#!/bin/sh

echo "Waiting for MySQL..."

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

echo "MySQL started"

python manage.py migrate
python manage.py collectstatic --noinput

gunicorn gamearena.wsgi:application --bind 0.0.0.0:8000 --reload