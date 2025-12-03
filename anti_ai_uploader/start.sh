#!/usr/bin/env bash
set -e

# ensure migrations exist and apply them
python manage.py makemigrations --noinput || true
python manage.py migrate --noinput

# (keep collectstatic disabled for debugging)
# run gunicorn
exec gunicorn anti_ai_uploader.wsgi:application --bind 0.0.0.0:$PORT --workers 2
