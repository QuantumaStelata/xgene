#!/bin/sh

python manage.py migrate

if ! python manage.py load_clan; then
    exit
fi

gunicorn cluster.wsgi -c DEV-etc/gunicorn.conf.py

exec "$@"
