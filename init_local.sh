#!/usr/bin/env bash
echo "[run] install requirements.txt"
pip install -r requirements.txt || exit 1

echo "[run] make migrations"
python3 ./backend/manage.py makemigrations || exit 1

echo "[run] Migrate DB"
python3 ./backend/manage.py migrate || exit 1

echo "[run] Create superuser"
echo "from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    user = User()
    user.first_name = 'Admin'
    user.last_name = 'Dev'
    user.is_superuser = True
    user.is_staff = True
    user.set_password('qwerty123')
    user.email = 'matiroson@gmail.com'
    user.username = 'admin'
    user.save()

from django.contrib.sites.models import Site
Site.objects.get_or_create(domain='0.0.0.0:8000', name='localhost')
" | ./backend/manage.py shell || exit 1

# echo "[run] Load Initial data"
# python3 manage.py loaddata /usr/src/app/fixtures/users.json || exit 1

echo "[run] runserver with django"
./backend/manage.py runserver 0.0.0.0:8000
