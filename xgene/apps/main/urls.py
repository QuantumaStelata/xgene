from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'news/(\d+)', views.article, name='article'),
    url(r'news', views.news, name='news'),
    url(r'players', views.players, name='players'),
    url(r'', views.main, name='main'),
]
