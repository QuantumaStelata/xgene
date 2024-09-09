#!/bin/sh

python manage.py migrate

if ! python manage.py update_clan; then
    exit
fi

if ! python manage.py telegram_setup; then
    exit
fi

gunicorn cluster.asgi -c DEV-etc/gunicorn.conf.py

exec "$@"
