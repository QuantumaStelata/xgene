from rest_framework import mixins, permissions, viewsets

from apps.core.api.v1.serializers.users import UserSerializer
from apps.core.models import User


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all().order_by('role', 'username')
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
