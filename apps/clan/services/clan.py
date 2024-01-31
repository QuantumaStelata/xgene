from django.conf import settings

from apps.clan.models import Clan
from generic.services.wargaming import WargamingRequestService


class ClanService:
    @classmethod
    def update_clan(cls):
        data = WargamingRequestService.get('wot/clans/info/', params={'clan_id': settings.CLAN_ID})
        clan = data['data'][str(settings.CLAN_ID)]
        Clan.objects.update_or_create(
            external_id=clan['clan_id'],
            defaults={
                'tag': clan['tag'],
                'name': clan['name'],
                'motto': clan['motto'],
                'color': clan['color'],
                'emblem': clan['emblems']['x195']['portal'],
            },
        )
