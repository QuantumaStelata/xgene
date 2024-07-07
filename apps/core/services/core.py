from django.conf import settings

from apps.core.models import User
from apps.directory.models import Role
from generic.services.wargaming import WargamingRequestService


class CoreService:
    @classmethod
    def update_users(cls):
        players = []
        roles = dict(Role.objects.values_list('external_id', 'id'))
        data = WargamingRequestService.get('wot/clans/info/', params={'clan_id': settings.CLAN_ID})

        for player in data['data'][str(settings.CLAN_ID)]['members']:
            players.append(
                User(
                    username=player['account_name'],
                    role_id=roles[player['role']],
                    external_id=player['account_id'],
                ),
            )

        clan_players = User.objects.bulk_create(
            players,
            update_conflicts=True,
            update_fields=['username', 'role_id'],
            unique_fields=['external_id'],
        )

        User.objects.exclude(external_id__in=[player.external_id for player in clan_players]).delete()
        return clan_players

    @classmethod
    def update_users_access_tokens(cls):
        users = User.objects.exclude(access_token='').iterator(chunk_size=100)
        updated_users = []

        for user in users:
            updated_users.append(cls.update_user_access_token(user, save=False))

        User.objects.bulk_update(updated_users, fields=['access_token'])

    @classmethod
    def update_user_access_token(cls, user: User, save: bool = True, access_token: str | None = None) -> User:
        data = WargamingRequestService.post(
            'wot/auth/prolongate/',
            json={'access_token': access_token or user.access_token},
        )

        if data.get('status') == 'ok' and data.get('data', {}).get('account_id') == user.external_id:
            user.access_token = data['data']['access_token']
        else:
            return cls.delete_user_access_token(user, save=save)

        if save:
            user.save(update_fields=['access_token'])

        return user

    @classmethod
    def delete_user_access_token(cls, user: User, save: bool = True) -> User:
        user.access_token = ''
        if hasattr(user, 'auth_token'):
            user.auth_token.delete()

        if save:
            user.save(update_fields=['access_token'])

        return user
