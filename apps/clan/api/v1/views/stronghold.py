from django.conf import settings
from rest_framework import mixins, permissions, viewsets

from apps.clan.api.v1.serializers.stronghold import StrongholdSerializer
from apps.clan.models import Stronghold


class StrongholdViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Stronghold.objects.all()
    serializer_class = StrongholdSerializer
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'clan__external_id'

    def get_object(self):
        self.kwargs[self.lookup_field] = settings.CLAN_ID
        return super().get_object()
