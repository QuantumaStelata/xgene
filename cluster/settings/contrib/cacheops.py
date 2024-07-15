from cluster.settings.django import REDIS_URL
from cluster.settings.environment import env

CACHEOPS = {
    'core.user': {'ops': 'get', 'timeout': 60 * 15},
    'auth.*': {'ops': {'fetch', 'get'}, 'timeout': 60 * 30},
    'authtoken.*': {'ops': {'fetch', 'get'}, 'timeout': 60 * 60 * 4},
    'directory.*': {'ops': 'all', 'timeout': 60 * 60 * 4},
    'marks.*': {'ops': 'all', 'timeout': 60 * 60 * 4},
    '*.*': {'ops': (), 'timeout': 60 * 60},
}

CACHEOPS_SKIP_FIELDS = ('FileField', 'TextField', 'BinaryField', 'JSONField')
CACHEOPS_REDIS = REDIS_URL + '/3'
CACHEOPS_ENABLED = env.bool('CACHEOPS_ENABLED', False)
