from rest_framework import mixins, permissions, viewsets

from apps.news.api.v1.serializers.comments import CommentSerializer
from apps.news.models import Comment


class CommentViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        queryset = super().get_queryset().filter(new_id=self.kwargs['new_pk'])
        if self.action != 'list':
            queryset = queryset.filter(author=self.request.user)
        return queryset

    def perform_create(self, serializer):
        return serializer.save(new_id=self.kwargs['new_pk'])
