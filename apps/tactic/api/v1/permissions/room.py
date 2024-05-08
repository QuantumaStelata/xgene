from rest_framework import permissions

from apps.directory.models import Role


class RoomPermission(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE' and (
            request.user != obj.author or
            request.user.role_id not in (
                Role.PrimaryID.COMMANDER,
                Role.PrimaryID.EXECUTIVE_OFFICER,
            )
        ):
            return False
        return True
