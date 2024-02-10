from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import action

from apps.core.api.v1.filters.users import UserFilter
from apps.core.api.v1.serializers.users import UserSerializer
from apps.core.models import User


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all().order_by('role', 'username')
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
    filterset_class = UserFilter

    @action(methods=['get'], detail=False, permission_classes=(permissions.IsAuthenticated,))
    def me(self, request, *args, **kwargs):
        self.kwargs[self.lookup_field] = request.user.id
        return self.retrieve(request, *args, **kwargs)
