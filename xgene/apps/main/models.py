# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models


class ClanId(models.Model):
    _id = models.TextField('ID клана', null=False, default=1)

    def __str__(self):
        return self._id

    class Meta:
        verbose_name = 'ID клана'
        verbose_name_plural = 'ID клана'

class ClanInfo(models.Model):
    clan_tag = models.TextField('Тэг клана', primary_key=True, default='Tag')
    clan_name = models.TextField('Название клана', null=True, default='Name')
    clan_motto = models.TextField('Девиз клана', null=True, default='Motto')
    clan_color = models.TextField('Цвет клана', null=True, default='#fff')
    clan_emblem = models.TextField('Эмблема клана', null=True, default=0)
    
    def __str__(self):
        return self.clan_tag

    class Meta:
        verbose_name = 'Информация о клане'
        verbose_name_plural = 'Информация о клане'

class ClanStatic(models.Model):
    clan_tag = models.ForeignKey(ClanInfo, on_delete = models.CASCADE)
    clan_sh10 = models.TextField('УРЭЛО 10', null=True, default=0)
    clan_sh8 = models.TextField('УРЭЛО 8', null=True, default=0)
    clan_sh6 = models.TextField('УРЭЛО 6', null=True, default=0)
    clan_gm10 = models.TextField('ГКЭЛО 10', null=True, default=0)
    clan_gm8 = models.TextField('ГКЭЛО 8', null=True, default=0)
    clan_gm6 = models.TextField('ГКЭЛО 6', null=True, default=0)
    clan_battles_count = models.TextField('Среднее кол-во боев', null=True, default=0)
    clan_win_rate = models.TextField('Среднее процент побед', null=True, default=0)
    clan_rate = models.TextField('Рейтинг клана', null=True, default=0)
    clan_position = models.TextField('Позиция клана', null=True, default=0)
    clan_xp_per_battle = models.TextField('Средний опыт за бой', null=True, default=0)
    clan_damage_per_battle = models.TextField('Средний урон за бой', null=True, default=0)
    clan_static_update = models.DateTimeField('Время обновления статистики', auto_now=True)

    def __str__(self):
        return self.clan_position

    class Meta:
        verbose_name = 'Статистика клане'
        verbose_name_plural = 'Статистика клане'


class ClanRole(models.Model):
    clan_role_ru = models.TextField('Должность игрока', null=True)

    def __str__(self):
        return self.clan_role_ru

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'
        ordering = ('id',)

class Players(models.Model):
    player_clan = models.ForeignKey(ClanId, on_delete = models.CASCADE, null=True)
    player_role = models.ForeignKey(ClanRole, on_delete = models.CASCADE, null=True)
    player_id = models.TextField('ID игрока', primary_key=True)
    player_name = models.TextField('Имя игрока', null=True)
    player_battles = models.TextField('Всего боев', null=True, default=0)
    player_wgr = models.TextField('WGR', null=True, default=0)
    player_win = models.TextField('Всего побед', null=True, default=0)
    player_damage = models.TextField('Всего дамага', null=True, default=0)
    player_frags = models.TextField('Всего фрагов', null=True, default=0)
    
    def __str__(self):
        return self.player_name

    class Meta:
        verbose_name = 'Игрок клана'
        verbose_name_plural = 'Игроки клана'
        ordering = ('player_role_id',)

class Article(models.Model):
    article_name = models.TextField('Название статьи')
    article_text = RichTextUploadingField('Текст статьи')
    article_date = models.DateTimeField('Дата публикации')
    article_publicate = models.BooleanField('Опубликовать?', default=False)

    def __str__(self):
        return self.article_name

    def __was__(self):
        return self.article_date

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
