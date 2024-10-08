from channels.routing import URLRouter
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularJSONAPIView, SpectacularSwaggerView

from apps.tactic.api.v1.urls import websocket_urlpatterns as tactic_websocket_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/clan/', include('apps.clan.api.v1.urls')),
    path('api/v1/core/', include('apps.core.api.v1.urls')),
    path('api/v1/directory/', include('apps.directory.api.v1.urls')),
    path('api/v1/marks/', include('apps.marks.api.v1.urls')),
    path('api/v1/tactic/', include('apps.tactic.api.v1.urls')),
    path('api/v1/news/', include('apps.news.api.v1.urls')),
    path('api/v1/integrations/telegram/', include('apps.integrations.telegram.api.v1.urls'), name='telegram'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.SWAGGER_URL:
    urlpatterns += [
        path(f'api/v1/{settings.SWAGGER_URL}.json', SpectacularJSONAPIView.as_view(), name='schema'),
        path(f'api/v1/{settings.SWAGGER_URL}', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    ]

websocket_urlpatterns = [
    path('api/v1/ws/tactic/', URLRouter(tactic_websocket_urlpatterns)),
]
