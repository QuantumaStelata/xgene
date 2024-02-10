import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

asgi_app = get_asgi_application()

from cluster.urls import websocket_urlpatterns  # noqa
from generic.authentications.channels import WebsocketTokenAuthMiddleware  # noqa

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cluster.settings')

application = ProtocolTypeRouter({
    'http': asgi_app,
    'websocket': WebsocketTokenAuthMiddleware(
        URLRouter(websocket_urlpatterns),
    ),
})
