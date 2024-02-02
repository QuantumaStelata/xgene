from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/clan/', include('apps.clan.api.v1.urls')),
    path('api/v1/core/', include('apps.core.api.v1.urls')),
    path('api/v1/directory/', include('apps.directory.api.v1.urls')),
    path('api/v1/marks/', include('apps.marks.api.v1.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
