from rest_framework import permissions

from apps.core.models import User


class RoomPermission(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE' and (
            request.user != obj.author or
            request.user.role not in (
                User.Role.COMMANDER,
                User.Role.EXECUTIVE_OFFICER,
            )
        ):
            return False
        return True
