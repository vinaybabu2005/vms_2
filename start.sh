#!/usr/bin/env bash
set -e
python manage.py migrate --noinput
python manage.py bootstrap_admin
python manage.py seed_products
exec gunicorn config.wsgi:application --bind "0.0.0.0:${PORT:-8000}"
