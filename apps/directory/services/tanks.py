import mimetypes

import requests
from django.conf import settings
from django.core.files.base import ContentFile

from apps.directory.models import Tank
from generic.services.wargaming import WargamingRequestService


class TankService:
    @classmethod
    def update_tanks(cls):
        tanks = []
        data = WargamingRequestService.get('wot/encyclopedia/vehicles/', params={'language': settings.WG_API_LANGUAGE})

        for _, value in data['data'].items():
            contour_url = value['images']['contour_icon']
            response = requests.get(contour_url)
            content_type = response.headers['Content-Type']
            extension = mimetypes.guess_extension(content_type)
            filename = str(value['tank_id']) + extension
            controur = ContentFile(response.content, name=filename)

            tanks.append(
                Tank(
                    name=value['name'],
                    level=value['tier'],
                    type=value['type'],
                    nation=value['nation'],
                    contour=controur,
                    external_id=value['tank_id'],
                ),
            )

        return Tank.objects.bulk_create(
            tanks,
            update_conflicts=True,
            update_fields=['name', 'level', 'type', 'nation', 'contour'],
            unique_fields=['external_id'],
        )
