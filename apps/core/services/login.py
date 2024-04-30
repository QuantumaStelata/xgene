from urllib.parse import urlencode

from django.conf import settings
from rest_framework.authtoken.models import Token

from apps.core.models import User
from apps.core.services.core import CoreService


class LoginService:
    @classmethod
    def get_openid_url(cls, redirect_uri: str | None = None) -> str:
        host = settings.WG_API_HOST

        if not redirect_uri:
            redirect_uri = f'{settings.FRONT_DOMAIN}login'

        params = urlencode({
            'application_id': settings.APPLICATION_ID,
            'redirect_uri': redirect_uri,
        })
        return f'{host}wot/auth/login/?{params}'

    @classmethod
    def login(cls, username: str, access_token: str, external_id: int) -> Token | None:
        try:
            user = User.objects.get(external_id=external_id, username=username)
        except User.DoesNotExist:
            return

        user = CoreService.update_user_access_token(user, access_token=access_token)
        if user.access_token:
            token, _ = Token.objects.get_or_create(user=user)
            return token
