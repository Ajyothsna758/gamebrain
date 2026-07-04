#!/bin/sh

python manage.py migrate
python manage.py collectstatic --noinput

python manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL")

if username and password and email:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print("Superuser created.")
    else:
        print("Superuser already exists.")
EOF

if [ -f data.json ]; then
    python manage.py loaddata data.json
fi


exec gunicorn gamearena.wsgi:application --bind 0.0.0.0:${PORT:-10000}