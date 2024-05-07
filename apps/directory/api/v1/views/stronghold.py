from rest_framework import mixins, permissions, viewsets

from apps.directory.api.v1.serializers.stronghold import StrongholdBuildTypeSerializer
from apps.directory.models import StrongholdBuildType


class StrongholdBuildTypeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = StrongholdBuildType.objects.all()
    serializer_class = StrongholdBuildTypeSerializer
    permission_classes = (permissions.AllowAny,)
