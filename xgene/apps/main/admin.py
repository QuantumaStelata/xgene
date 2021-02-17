# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

admin.site.register(ClanId)

@admin.register(ClanStatic)
class ClanStaticAdmin(admin.ModelAdmin):
    list_display = ('clan_tag', 'clan_static_update')


@admin.register(ClanInfo)
class ClanInfoAdmin(admin.ModelAdmin):
    list_display = ('clan_tag', 'clan_name', 'clan_motto')
    fields = ('clan_tag', 'clan_name', 'clan_motto', 'clan_color',)

admin.site.register(ClanRole)

@admin.register(Players)
class PlayersAdmin(admin.ModelAdmin):
    list_display = ('player_name', 'player_role')
    fields = ('player_name', 'player_id', ('player_clan', 'player_role'),)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('article_name', 'article_date', 'article_publicate')
