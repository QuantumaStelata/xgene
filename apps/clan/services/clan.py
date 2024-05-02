import mimetypes

import requests
from django.conf import settings
from django.core.files.base import ContentFile

from apps.clan.models import Clan
from generic.services.wargaming import WargamingRequestService


class ClanService:
    @classmethod
    def update_clan(cls):
        data = WargamingRequestService.get('wot/clans/info/', params={'clan_id': settings.CLAN_ID})
        clan = data['data'][str(settings.CLAN_ID)]

        emblem_url = clan['emblems']['x195']['portal']
        response = requests.get(emblem_url)
        content_type = response.headers['Content-Type']
        extension = mimetypes.guess_extension(content_type)
        filename = str(clan['clan_id']) + extension
        emblem = ContentFile(response.content, name=filename)

        clan, _ = Clan.objects.update_or_create(
            external_id=clan['clan_id'],
            defaults={
                'tag': clan['tag'],
                'name': clan['name'],
                'motto': clan['motto'],
                'color': clan['color'],
                'emblem': emblem,
            },
        )
        return clan
