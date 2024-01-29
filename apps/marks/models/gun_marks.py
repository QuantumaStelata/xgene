from django.db import models

from mixins.models import DateTimeMixin


class GunMark(DateTimeMixin):
    tank = models.OneToOneField('directory.Tank', on_delete=models.CASCADE, related_name='gun_mark')
    mark_20 = models.IntegerField()
    mark_30 = models.IntegerField()
    mark_40 = models.IntegerField()
    mark_50 = models.IntegerField()
    mark_55 = models.IntegerField()
    mark_60 = models.IntegerField()
    mark_65 = models.IntegerField()
    mark_70 = models.IntegerField()
    mark_75 = models.IntegerField()
    mark_80 = models.IntegerField()
    mark_85 = models.IntegerField()
    mark_90 = models.IntegerField()
    mark_95 = models.IntegerField()
    mark_100 = models.IntegerField()
