from django.conf import settings
from rest_framework import mixins, permissions, viewsets

from apps.clan.api.v1.serializers.clan import ClanSerializer
from apps.clan.models import Clan


class ClanViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Clan.objects.all()
    serializer_class = ClanSerializer
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'external_id'

    def get_object(self):
        self.kwargs[self.lookup_field] = settings.CLAN_ID
        return super().get_object()
