#!/bin/sh
set -e

echo "STEP 1"
python manage.py migrate

echo "STEP 2"
python manage.py collectstatic --noinput

echo "STEP 3"
python manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()

username=os.getenv("DJANGO_SUPERUSER_USERNAME")
password=os.getenv("DJANGO_SUPERUSER_PASSWORD")
email=os.getenv("DJANGO_SUPERUSER_EMAIL")

if username and password and email:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username,email,password)
        print("Created")
    else:
        print("Exists")
EOF


echo "STEP 4"

echo "Starting Gunicorn"

exec gunicorn gamearena.wsgi:application \
    --bind 0.0.0.0:${PORT:-10000}