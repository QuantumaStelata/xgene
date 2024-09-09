from django.core.exceptions import ImproperlyConfigured

from cluster.settings.environment import env

TELEGRAM_API_KEY = env.str('TELEGRAM_API_KEY', '')
TELEGRAM_API_SECRET = env.str('TELEGRAM_API_SECRET', '')
TELEGRAM_BOT_USERNAME = env.str('TELEGRAM_BOT_USERNAME', '')

if TELEGRAM_API_KEY and not all((TELEGRAM_API_SECRET, TELEGRAM_BOT_USERNAME)):
    raise ImproperlyConfigured('You must specify TELEGRAM_API_SECRET and TELEGRAM_BOT_USERNAME in the .env file')
