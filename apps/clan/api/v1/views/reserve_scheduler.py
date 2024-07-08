from rest_framework import viewsets

from apps.clan.api.v1.permissions.reserve_scheduler import ReserveSchedulerPermission
from apps.clan.api.v1.serializers.reserve_scheduler import ReserveSchedulerSerializer, ReserveSerializer
from apps.clan.models import Reserve, ReserveScheduler


class ReserveSchedulerViewSet(viewsets.ModelViewSet):
    queryset = Reserve.objects.prefetch_related('schedulers').filter(
        disposable=False,
        schedulers__isnull=False,
    ).distinct()
    serializer_class = ReserveSerializer
    create_serializer_class = ReserveSchedulerSerializer
    permission_classes = (ReserveSchedulerPermission,)

    def get_serializer_class(self):
        if self.action == 'create':
            return self.create_serializer_class
        return super().get_serializer_class()

    def get_queryset(self):
        if self.action == 'destroy':
            return ReserveScheduler.objects.all()
        from apps.clan.services.reserve import ReserveService
        ReserveService.activate_schedule_reserves()
        return super().get_queryset()
