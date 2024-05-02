from cluster.settings.contrib import *  # noqa: F401, F403
from cluster.settings.django import *  # noqa: F401, F403
from cluster.settings.project import *  # noqa: F401, F403

CELERY_RESULT_BACKEND = None
CELERY_BROKER_URL = 'memory://'

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
}

CACHEOPS_ENABLED = False

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}
