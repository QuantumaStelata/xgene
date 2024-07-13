from rest_framework.routers import DynamicRoute, Route
from rest_framework_nested.routers import NestedSimpleRouter


class NestedWithoutLookUpRouter(NestedSimpleRouter):
    routes = [
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'post': 'create',
                'get': 'list',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy',
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'},
        ),
        # Dynamically generated detail routes. Generated using
        # @action(detail=True) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={},
        ),
    ]
