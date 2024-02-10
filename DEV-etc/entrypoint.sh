#!/bin/sh

python manage.py migrate

if ! python manage.py update_clan; then
    exit
fi

gunicorn cluster.asgi -c DEV-etc/gunicorn.conf.py

exec "$@"
