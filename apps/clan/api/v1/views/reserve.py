from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.clan.api.v1.permissions.reserve import ActivateReservePermission
from apps.clan.api.v1.serializers.reserve import ReserveSerializer
from apps.clan.models import Reserve
from apps.clan.services.reserve import ReserveService


class ReserveViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Reserve.objects.all()
    serializer_class = ReserveSerializer

    @action(methods=['get'], detail=True, permission_classes=(ActivateReservePermission,))
    def activate(self, request, *args, **kwargs):
        reserve = self.get_object()
        activated = ReserveService.activate_reserve(user=request.user, reserve=reserve)
        return Response({'activated': activated})

    @action(methods=['get'], detail=False, permission_classes=(ActivateReservePermission,))
    def can_activate(self, request, *args, **kwargs):
        return Response({'status': 'ok'})
