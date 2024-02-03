from django.db import models

from mixins.models import DateTimeMixin


class GunMark(DateTimeMixin):
    tank = models.OneToOneField('directory.Tank', on_delete=models.CASCADE, related_name='gun_mark')
    mark_20 = models.PositiveSmallIntegerField()
    mark_30 = models.PositiveSmallIntegerField()
    mark_40 = models.PositiveSmallIntegerField()
    mark_50 = models.PositiveSmallIntegerField()
    mark_55 = models.PositiveSmallIntegerField()
    mark_60 = models.PositiveSmallIntegerField()
    mark_65 = models.PositiveSmallIntegerField()
    mark_70 = models.PositiveSmallIntegerField()
    mark_75 = models.PositiveSmallIntegerField()
    mark_80 = models.PositiveSmallIntegerField()
    mark_85 = models.PositiveSmallIntegerField()
    mark_90 = models.PositiveSmallIntegerField()
    mark_95 = models.PositiveSmallIntegerField()
    mark_100 = models.PositiveSmallIntegerField()
