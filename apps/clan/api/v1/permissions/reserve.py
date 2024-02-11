from rest_framework import permissions

from apps.core.models import User


class ActivateReservePermission(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.access_token and request.user.role in [
            User.Role.COMMANDER,
            User.Role.EXECUTIVE_OFFICER,
        ]
