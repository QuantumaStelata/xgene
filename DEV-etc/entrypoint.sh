#!/bin/sh

python manage.py migrate
gunicorn cluster.wsgi -c DEV-etc/gunicorn.conf.py

exec "$@"
