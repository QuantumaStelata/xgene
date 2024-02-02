import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cluster.settings')

app = Celery('cluster')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {
    'update-gun-marks': {
        'task': 'apps.marks.tasks.marks.update_gun_marks',
        'schedule': crontab(minute=0, hour=1),
    },
    'update-mastery': {
        'task': 'apps.marks.tasks.marks.update_mastery',
        'schedule': crontab(minute=0, hour=1),
    },
    'update-tanks': {
        'task': 'apps.directory.tasks.tanks.update_tanks',
        'schedule': crontab(minute=0, hour=2),
    },
    'update-clan': {
        'task': 'apps.clan.tasks.clan.update_clan',
        'schedule': crontab(minute='*/15'),
    },
    'update-users': {
        'task': 'apps.core.tasks.core.update_users',
        'schedule': crontab(minute='*/15'),
    },
    'update-stronghold': {
        'task': 'apps.clan.tasks.stronghold.update_stronghold',
        'schedule': crontab(minute=0, hour='*/1'),
    },
}

app.autodiscover_tasks()
