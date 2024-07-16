from django.db.models import Count
from rest_framework import permissions, viewsets

from apps.news.api.v1.filters.news import NewFilter
from apps.news.api.v1.serializers.news import NewSerializer
from apps.news.models import New
from apps.news.tasks import add_new_viewer


class NewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = New.objects.annotate(viewers_count=Count('viewers')).all()
    serializer_class = NewSerializer
    permission_classes = (permissions.AllowAny,)
    filterset_class = NewFilter

    def retrieve(self, request, *args, **kwargs):
        add_new_viewer.s(new=self.kwargs['pk'], user=self.request.user.id).apply_async()
        return super().retrieve(request, *args, **kwargs)
