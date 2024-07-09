from rest_framework import permissions

from apps.directory.models import Role


class ReserveSchedulerPermission(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.access_token and request.user.role_id in (
            Role.PrimaryID.COMMANDER,
            Role.PrimaryID.EXECUTIVE_OFFICER,
        )
