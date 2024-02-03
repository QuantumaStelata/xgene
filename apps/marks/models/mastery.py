from django.db import models

from mixins.models import DateTimeMixin


class Mastery(DateTimeMixin):
    tank = models.OneToOneField('directory.Tank', on_delete=models.CASCADE, related_name='mastery')
    class_3 = models.PositiveSmallIntegerField()
    class_2 = models.PositiveSmallIntegerField()
    class_1 = models.PositiveSmallIntegerField()
    master = models.PositiveSmallIntegerField()
