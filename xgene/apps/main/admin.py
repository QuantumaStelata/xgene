# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

admin.site.register(ClanId)

@admin.register(ClanName)
class ClanNameAdmin(admin.ModelAdmin):
    list_display = ('clan_name', 'clan_motto')

admin.site.register(ClanRole)

@admin.register(Players)
class PlayersAdmin(admin.ModelAdmin):
    list_display = ('player_name', 'player_role')
    fields = ('player_name', 'player_id', ('player_clan', 'player_role'),)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('article_name', 'article_date', 'article_publicate')


