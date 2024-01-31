from apps.directory.models import Tank
from generic.services.wargaming import WargamingRequestService


class TankService:
    @classmethod
    def update_tanks(cls):
        tanks = []
        data = WargamingRequestService.get('wot/encyclopedia/vehicles/')

        for _, value in data['data'].items():
            tanks.append(
                Tank(
                    name=value['name'],
                    level=value['tier'],
                    type=value['type'],
                    nation=value['nation'],
                    contour=value['images']['contour_icon'],
                    external_id=value['tank_id'],
                ),
            )

        Tank.objects.bulk_create(
            tanks,
            update_conflicts=True,
            update_fields=['name', 'level', 'type', 'nation', 'contour'],
            unique_fields=['external_id'],
        )
