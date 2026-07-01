#!/bin/sh

python manage.py migrate
python manage.py collectstatic --noinput

python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()

username = "admin"
password = "shiva@1234"
email = "admin@example.com"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
EOF

exec "$@"