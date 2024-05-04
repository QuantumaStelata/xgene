from django.conf import settings

from apps.clan.models import Build, Clan, Stronghold
from apps.directory.models import Map, ReserveType
from generic.services.wargaming import WargamingRequestService


class StrongholdService:
    @classmethod
    def update_stronghold(cls):
        data = WargamingRequestService.get('wot/stronghold/claninfo/', params={'clan_id': settings.CLAN_ID})
        stronghold_data = data['data'][str(settings.CLAN_ID)]

        clan = Clan.objects.only('id').get(external_id=stronghold_data['clan_id'])
        maps = dict(Map.objects.values_list('external_id', 'id'))
        reserve_types = dict(ReserveType.objects.values_list('external_id', 'id'))

        stronghold, _ = Stronghold.objects.update_or_create(
            clan=clan,
            defaults={
                'level': stronghold_data['stronghold_level'],
                'map_id': maps.get(stronghold_data['command_center_arena_id']),
            },
        )

        builds = [
            Build(
                stronghold=stronghold,
                direction=build['direction'],
                position=build['position'],
                title=build['building_title'],
                level=build['building_level'],
                map_id=maps.get(build['arena_id']),
                reserve_type_id=reserve_types.get(build['reserve_title']),
            ) for build in stronghold_data['building_slots']
        ]

        Build.objects.bulk_create(
            builds,
            update_conflicts=True,
            update_fields=['title', 'level', 'map', 'reserve_type'],
            unique_fields=['stronghold', 'direction', 'position'],
        )
