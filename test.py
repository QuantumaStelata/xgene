import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cluster.settings')

import django
django.setup()

from django.conf import settings
import requests
import pprint
data = {
    'application_id': settings.APPLICATION_ID,
    'language': 'ru'
}
a = set()
r = requests.post(f'{settings.WG_API_HOST}wot/encyclopedia/vehicles/', data=data)
data = r.json()['data']

for _, value in data.items():
    pprint.pprint(value)
    break
print(a)
