from django.conf import settings
from django.http.response import HttpResponseRedirect
from rest_framework import generics, permissions
from rest_framework.response import Response

from apps.core.api.v1.serializers.login import LoginSerializer
from apps.telegram.api.v1.permissions.telegram import TelegramPermission
from apps.telegram.api.v1.services.telegram import TelegramService


class TelegramView(generics.GenericAPIView):
    permission_classes = (TelegramPermission,)

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        if 'callback_query' in request.data:
            data = data['callback_query']
        TelegramService.parse_message(data['message'])
        return Response()


class TelegramLoginView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def get(self, request, user_id, *args, **kwargs):
        serializer = self.get_serializer(
            data={
                'username': request.GET.get('nickname'),
                'external_id': request.GET.get('account_id'),
                'access_token': request.GET.get('access_token'),
            },
        )
        serializer.is_valid()
        TelegramService.auth(
            user_id=user_id,
            username=serializer.validated_data['username'],
            access_token=serializer.validated_data['access_token'],
            external_id=serializer.validated_data['external_id'],
        )
        return HttpResponseRedirect(f'https://t.me/{settings.TELEGRAM_BOT_USERNAME}')
