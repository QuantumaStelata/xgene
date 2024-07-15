import contextlib

from rest_framework import mixins, permissions, viewsets

from apps.news.api.v1.paginations.reactions import ReactionPagination
from apps.news.api.v1.serializers.reactions import ReactionSerializer
from apps.news.models import Reaction


class ReactionViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Reaction.objects.select_related('author').all()
    serializer_class = ReactionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = ReactionPagination
    lookup_field = 'author'

    def get_object(self):
        self.kwargs['author'] = self.request.user
        return super().get_object()

    def get_queryset(self):
        return super().get_queryset().filter(new_id=self.kwargs['new_pk'])

    def perform_create(self, serializer):
        with contextlib.suppress(Reaction.DoesNotExist):
            serializer.instance = self.get_queryset().get(author=self.request.user)

        serializer.save(new_id=int(self.kwargs['new_pk']))
