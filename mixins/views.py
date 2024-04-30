from rest_framework import exceptions, serializers, views, viewsets


class NestedViewSet(viewsets.GenericViewSet):
    nested_lookup_field: str = 'nested_1'
    nested_view: views.APIView = None

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        self.nested_object = self.get_nested_object()
        self.check_nested_object_permissions(request=request, obj=self.nested_object)

    @property
    def nested_lookup(self):
        return {self.nested_lookup_field: self.nested_object}

    def get_nested_object(self):
        if self.nested_view and self.nested_lookup_field:
            nested_pk = self.kwargs[f'{self.nested_lookup_field}_pk']
            try:
                return self.nested_view.queryset.get(pk=nested_pk)
            except self.nested_view.queryset.model.DoesNotExist:
                raise exceptions.NotFound()

    def get_nested_permissions(self):
        return [permission() for permission in self.nested_view.permission_classes]

    def check_nested_object_permissions(self, request, obj):
        for permission in self.get_nested_permissions():
            if not permission.has_object_permission(request, self, obj):
                self.permission_denied(
                    request,
                    message=getattr(permission, 'message', None),
                    code=getattr(permission, 'code', None),
                )

    def get_queryset(self):
        return super().get_queryset().filter(**self.nested_lookup)

    def perform_create(self, serializer):
        serializer.save(**self.nested_lookup)

    def perform_update(self, serializer):
        serializer.save(**self.nested_lookup)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(self.nested_lookup)
        return context


class ActionSerializerViewSet(viewsets.GenericViewSet):
    list_serializer_class: serializers.Serializer = None
    retrieve_serializer_class: serializers.Serializer = None
    create_serializer_class: serializers.Serializer = None
    update_serializer_class: serializers.Serializer = None

    def get_serializer_class(self):
        if self.action == 'list' and self.list_serializer_class:
            return self.list_serializer_class
        elif self.action == 'retrieve' and self.retrieve_serializer_class:
            return self.retrieve_serializer_class
        elif self.action == 'create' and self.create_serializer_class:
            return self.create_serializer_class
        elif self.action in ('update', 'partial_update') and self.update_serializer_class:
            return self.update_serializer_class
        return super().get_serializer_class()
