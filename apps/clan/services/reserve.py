from django.conf import settings

from apps.clan.models import Reserve
from apps.core.models import User
from apps.directory.models import ReserveType
from generic.services.wargaming import WargamingRequestService
from generic.utils import unix_to_datetime


class ReserveService:
    @classmethod
    def update_reserves(cls):
        user = User.objects.exclude(access_token='').first()

        if not user:
            return

        data = WargamingRequestService.get(
            'wot/stronghold/clanreserves/',
            params={'clan_id': settings.CLAN_ID, 'access_token': user.access_token},
        )

        reserves = []
        reserves_data = data['data']
        reserve_types = dict(ReserveType.objects.values_list('external_id', 'id'))

        for reserve in reserves_data:
            for stock in reserve['in_stock']:
                disposable = reserve['disposable']
                clan_bonus = stock['bonus_values'][0]['value'] if not disposable else None
                random_bonus = stock['bonus_values'][-1]['value'] if not disposable else None
                activated_at = unix_to_datetime(stock['activated_at']) if stock['activated_at'] else None
                active_till = unix_to_datetime(stock['active_till']) if stock['active_till'] else None
                ready_to_activate = stock['status'] == 'ready_to_activate'

                reserves.append(
                    Reserve(
                        type_id=reserve_types[reserve['type']],
                        level=stock['level'],
                        count=stock['amount'],
                        clan_bonus=clan_bonus,
                        random_bonus=random_bonus,
                        activated_at=activated_at,
                        active_till=active_till,
                        disposable=disposable,
                        ready_to_activate=ready_to_activate,
                        x_level_only=stock['x_level_only'],
                    ),
                )

        Reserve.objects.bulk_create(
            reserves,
            update_conflicts=True,
            update_fields=[
                'count', 'clan_bonus', 'random_bonus', 'activated_at',
                'active_till', 'disposable', 'ready_to_activate', 'x_level_only',
            ],
            unique_fields=['type', 'level'],
        )
        Reserve.objects.filter(count__lte=0, active_till__isnull=True, activated_at__isnull=True).delete()

    @classmethod
    def activate_reserve(cls, user: User, reserve: Reserve) -> bool:
        if not user.access_token:
            return False

        data = WargamingRequestService.post(
            'wot/stronghold/activateclanreserve/',
            json={
                'clan_id': settings.CLAN_ID,
                'access_token': user.access_token,
                'reserve_level': reserve.level,
                'reserve_type': reserve.type.external_id,
            },
        )

        cls.update_reserves()
        return data.get('status') == 'ok'
