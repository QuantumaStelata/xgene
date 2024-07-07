import mimetypes

import requests
from django.conf import settings
from django.core.files.base import ContentFile

from apps.directory.models import Tank
from generic.services.wargaming import WargamingRequestService


class TankService:
    @classmethod
    def update_tanks(cls, with_translations=True):
        tanks = []

        data = WargamingRequestService.get(
            'wot/encyclopedia/vehicles/',
            params={
                'language': settings.MODELTRANSLATION_DEFAULT_LANGUAGE,
                'fields': 'name,tier,type,nation,tank_id,images',
            },
        )

        for value in data['data'].values():
            contour_url = value['images']['contour_icon']
            response = requests.get(contour_url)
            content_type = response.headers['Content-Type']
            extension = mimetypes.guess_extension(content_type)
            filename = str(value['tank_id']) + extension
            contour = ContentFile(response.content, name=filename)

            tanks.append(
                Tank(
                    name=value['name'],
                    level=value['tier'],
                    type=value['type'],
                    nation=value['nation'],
                    contour=contour,
                    external_id=value['tank_id'],
                ),
            )

        Tank.objects.bulk_create(
            tanks,
            update_conflicts=True,
            update_fields=['name', 'level', 'type', 'nation', 'contour'],
            unique_fields=['external_id'],
        )

        if with_translations:
            cls.update_tanks_translation()

    @classmethod
    def update_tanks_translation(cls):
        tank_id_map = dict(Tank.objects.values_list('external_id', 'id'))

        for language in settings.MODELTRANSLATION_LANGUAGES:
            tanks = []

            data = WargamingRequestService.get(
                'wot/encyclopedia/vehicles/',
                params={
                    'language': language,
                    'fields': 'name,tank_id',
                },
            )

            for value in data['data'].values():
                tank_id = tank_id_map.get(value['tank_id'])

                if not tank_id:
                    continue

                tank_data = {f'name_{language}': value['name']}
                tanks.append(Tank(id=tank_id, **tank_data))

            Tank.objects.bulk_update(tanks, fields=[f'name_{language}'])
