import requests

from apps.core.models import User
from apps.directory.models import Tank
from generic.services.wargaming import WargamingRequestService


class UserService:
    TANKS_FIELDS = ('max_damage_tank_id', 'max_frags_tank_id', 'max_xp_tank_id')
    PRIVATE_FIELDS = ('credits', 'bonds', 'gold', 'free_xp')
    GENERIC_FIELDS = (
        'battles', 'wins', 'draws', 'losses', 'max_damage', 'max_frags', 'max_xp', 'frags',
        'spotted', 'dropped_capture_points', 'damage_dealt', 'damage_received', 'shots', 'hits',
    )

    @classmethod
    def update_users_stats(cls):
        users = User.objects.all()
        bulk_users = []

        for user in users:
            cls.update_user_stats(user=user, save=False)
            cls.update_user_wn8(user=user, save=False)
            bulk_users.append(user)

        fields = cls.PRIVATE_FIELDS + cls.GENERIC_FIELDS + cls.TANKS_FIELDS + ('wn8',)
        User.objects.bulk_update(bulk_users, fields=fields)

    @classmethod
    def update_user_stats(cls, user: User, save: bool = True) -> None:
        params = {'account_id': user.external_id, 'fields': 'statistics.all,private'}

        if user.access_token:
            params['access_token'] = user.access_token

        response = WargamingRequestService.get('wot/account/info/', params=params)
        if response['status'] == 'error':
            if 'access_token' in params:
                del params['access_token']
            else:
                return

            response = WargamingRequestService.get('wot/account/info/', params=params)

        data = response['data'][str(user.external_id)]

        for field in cls.PRIVATE_FIELDS:
            if not data.get('private'):
                break

            if value := data['private'].get(field):
                setattr(user, field, value)

        for field in cls.GENERIC_FIELDS:
            value = data['statistics']['all'][field]
            setattr(user, field, value)

        for field in cls.TANKS_FIELDS:
            value = data['statistics']['all'][field]
            if tank := Tank.objects.filter(external_id=value).first():
                setattr(user, field, tank.id)

        if save:
            user.save()

    @classmethod
    def update_user_wn8(cls, user: User, save: bool = True) -> None:
        params = {'account_id': user.external_id, 'extra': 'random', 'fields': 'tank_id,all'}
        response = WargamingRequestService.get('wot/tanks/stats/', params=params)
        wn8_reponse = requests.get('https://static.modxvm.com/wn8-data-exp/json/wn8exp.json')

        data = response['data'][str(user.external_id)]
        wn8_data = {tank['IDNum']: tank for tank in wn8_reponse.json()['data']}

        exp_dmg = 0
        exp_spot = 0
        exp_frag = 0
        exp_def = 0
        exp_win = 0

        for battle in ['all']:
            for tank in data:
                if not tank[battle]['battles']:
                    continue

                tank_id = tank['tank_id']

                if not wn8_data.get(tank_id):
                    continue

                exp_dmg += wn8_data[tank_id]['expDamage'] * tank[battle]['battles']
                exp_spot += wn8_data[tank_id]['expSpot'] * tank[battle]['battles']
                exp_frag += wn8_data[tank_id]['expFrag'] * tank[battle]['battles']
                exp_def += wn8_data[tank_id]['expDef'] * tank[battle]['battles']
                exp_win += wn8_data[tank_id]['expWinRate'] * tank[battle]['battles'] / 100

        r_damage = user.damage_dealt / exp_dmg
        r_spot = user.spotted / exp_spot
        r_frag = user.frags / exp_frag
        r_def = user.dropped_capture_points / exp_def
        r_win = user.wins / exp_win

        r_win_c = max(0, (r_win - 0.71) / (1 - 0.71))
        r_damage_c = max(0, (r_damage - 0.22) / (1 - 0.22))
        r_frag_c = min(r_damage_c + 0.2, max(0, (r_frag - 0.12) / (1 - 0.12)))
        r_spot_c = min(r_damage_c + 0.1, max(0, (r_spot - 0.38) / (1 - 0.38)))
        r_def_c = min(r_damage_c + 0.1, max(0, (r_def - 0.10) / (1 - 0.10)))

        user.wn8 = (
            980 * r_damage_c +
            210 * r_damage_c * r_frag_c +
            155 * r_frag_c * r_spot_c +
            75 * r_def_c * r_frag_c +
            145 * min(1.8, r_win_c)
        )

        if save:
            user.save()
