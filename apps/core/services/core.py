from django.conf import settings

from apps.core.models import User
from generic.services.wargaming import WargamingRequestService


class CoreService:
    @classmethod
    def update_users(cls):
        players = []
        data = WargamingRequestService.get('wot/clans/info/', params={'clan_id': settings.CLAN_ID})
        print(data)
        for player in data['data'][str(settings.CLAN_ID)]['members']:
            players.append(
                User(
                    username=player['account_name'],
                    role=User.ROLE_MAP[player['role']],
                    external_id=player['account_id'],
                ),
            )

        clan_players = User.objects.bulk_create(
            players,
            update_conflicts=True,
            update_fields=['username', 'role'],
            unique_fields=['external_id'],
        )
        User.objects.exclude(external_id__in=[player.external_id for player in clan_players]).delete()
