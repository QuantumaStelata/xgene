from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url('grappelli/', include('grappelli.urls')),
    url(r'^admin', admin.site.urls),
    url('', include('main.urls')),
]
