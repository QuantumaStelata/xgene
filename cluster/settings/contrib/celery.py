from cluster.settings.django import REDIS_URL
from cluster.settings.django import TIME_ZONE as DJANGO_TIME_ZONE

CELERY_BROKER_URL = REDIS_URL + '/4'
CELERY_RESULT_BACKEND = REDIS_URL + '/5'
CELERY_ACCEPT_CONTENT = [
    'application/json', 'json', 'pickle', 'application/x-python-serialize', 'application/x-pickle2',
]
CELERY_TASK_SERIALIZER = CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = DJANGO_TIME_ZONE

CELERY_BEAT_SCHEDULER = {}
