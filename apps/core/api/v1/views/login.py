from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.api.v1.serializers.login import LoginSerializer, OpenIdSerializer, TokenSerializer
from apps.core.models import User
from apps.core.services.login import LoginService


class LoginViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)

    @action(methods=['get'], detail=False, serializer_class=OpenIdSerializer)
    def openid(self, request, *args, **kwargs):
        url = LoginService.get_openid_url()
        serializer = self.get_serializer({'url': url})
        return Response(serializer.data)

    @action(methods=['post'], detail=False, serializer_class=LoginSerializer)
    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = LoginService.login(
            username=serializer.validated_data['username'],
            access_token=serializer.validated_data['access_token'],
            external_id=serializer.validated_data['external_id'],
        )
        if not token:
            return Response({'status': 'error'})

        token_serializer = TokenSerializer(instance=token)
        return Response(token_serializer.data)
