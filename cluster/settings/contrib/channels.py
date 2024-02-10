from cluster.settings.django import REDIS_URL

CHANNEL_LAYERS_REDIS_URL = REDIS_URL + '/6'


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(CHANNEL_LAYERS_REDIS_URL)],
        },
    },
}
