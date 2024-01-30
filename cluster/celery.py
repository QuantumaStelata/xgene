import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cluster.settings')

app = Celery('cluster')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {
    'update-gun-marks': {
        'task': 'apps.marks.tasks.marks.update_gun_marks',
        'schedule': crontab(minute='0'),
    },
    'update-mastery': {
        'task': 'apps.marks.tasks.marks.update_mastery',
        'schedule': crontab(minute='0'),
    },
}

app.autodiscover_tasks()
