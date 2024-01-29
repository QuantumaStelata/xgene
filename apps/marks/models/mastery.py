from django.db import models

from mixins.models import DateTimeMixin


class Mastery(DateTimeMixin):
    tank = models.OneToOneField('directory.Tank', on_delete=models.CASCADE, related_name='mastery')
    class_3 = models.IntegerField()
    class_2 = models.IntegerField()
    class_1 = models.IntegerField()
    master = models.IntegerField()
