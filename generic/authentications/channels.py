from urllib.parse import parse_qs

from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token


class WebsocketTokenAuthMiddleware:
    def __init__(self, app):
        self.app = app
        self.error_text = ''

    async def __call__(self, scope, receive, send):
        token = self.get_token(scope)
        scope['user'] = await self.get_user(token)
        scope['send'] = self.error_text
        return await self.app(scope, receive, send)

    def get_token(self, scope):
        query_string = scope['query_string']
        query_params = query_string.decode()
        query_dict = parse_qs(query_params)
        if token := query_dict.get('token'):
            return token[0]

    async def get_user(self, token):
        if not token:
            return AnonymousUser()

        try:
            token = await Token.objects.select_related('user').aget(key=token)
        except Token.DoesNotExist:
            return AnonymousUser()

        return token.user
