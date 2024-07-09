from rest_framework import viewsets

from apps.clan.api.v1.permissions.reserve_scheduler import ReserveSchedulerPermission
from apps.clan.api.v1.serializers.reserve_scheduler import ReserveSchedulerSerializer, ReserveSerializer
from apps.clan.models import Reserve, ReserveScheduler


class ReserveSchedulerViewSet(viewsets.ModelViewSet):
    queryset = Reserve.objects.prefetch_related('schedulers').filter(
        disposable=False,
        schedulers__isnull=False,
    ).distinct()
    reserve_scheduler_queryset = ReserveScheduler.objects.all()
    serializer_class = ReserveSerializer
    reserve_scheduler_serializer_class = ReserveSchedulerSerializer
    permission_classes = (ReserveSchedulerPermission,)

    def get_serializer_class(self):
        if self.action == 'list':
            return super().get_serializer_class()
        return self.reserve_scheduler_serializer_class

    def get_queryset(self):
        if self.action == 'list':
            return super().get_queryset()
        return self.reserve_scheduler_queryset
