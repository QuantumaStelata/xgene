from generic.services.wg import WGAPI
from apps.directory.models import Tank, Clan, Player
from django.conf import settings


class Synchronize:
    @classmethod
    def tanks(cls):
        tanks = []
        data = WGAPI.post('wot/encyclopedia/vehicles/')

        for _, value in data['data'].items():
            tanks.append(
                Tank(
                    name=value['name'],
                    level=value['tier'],
                    type=value['type'],
                    nation=value['nation'],
                    tank_id=value['tank_id'],
                ),
            )

        Tank.objects.bulk_create(
            tanks,
            update_conflicts=True,
            update_fields=['name', 'level', 'type', 'nation'],
            unique_fields=['tank_id'],
        )

    @classmethod
    def clan_data(cls):
        data = WGAPI.post('wot/clans/info/', clan_id=settings.CLAN_ID)
        clan = data['data'][str(settings.CLAN_ID)]

        Clan.objects.update_or_create(
            clan_id=clan['clan_id'],
            defaults={
                'tag': clan['tag'],
                'name': clan['name'],
                'motto': clan['motto'],
                'color': clan['color'],
                'emblem': clan['emblems']['x195']['portal'],
            }
        )

    @classmethod
    def clan_players(cls):
        players = []
        data = WGAPI.post('wot/clans/info/', clan_id=settings.CLAN_ID, language='ru')

        for player in data['data'][str(settings.CLAN_ID)]['members']:
            players.append(
                Player(
                    name=player['account_name'],
                    role=Player.ROLE_MAP[player['role']],
                    account_id=player['account_id'],
                )
            )

        players = Player.objects.bulk_create(
            players,
            update_conflicts=True,
            update_fields=['name', 'role'],
            unique_fields=['account_id'],
        )

        print(Player.objects.all() | players)
        # Player.objects.filter(account_id__in)
