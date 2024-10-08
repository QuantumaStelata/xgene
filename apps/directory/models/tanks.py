from django.db import models

from generic.storages import OverWriteStorage
from mixins.models import DateTimeMixin, ExternalIDMixin


class Tank(DateTimeMixin, ExternalIDMixin):
    class Type(models.TextChoices):
        SPG = 'SPG', 'САУ'
        AT_SPG = 'AT-SPG', 'ПТ-САУ'
        LIGHT = 'lightTank', 'Легкий танк'
        MEDIUM = 'mediumTank', 'Средний танк'
        HEAVY = 'heavyTank', 'Тяжелый танк'

    class Nation(models.TextChoices):
        USSR = 'ussr', 'СССР'
        GERMANY = 'germany', 'Германия'
        USA = 'usa', 'США'
        UK = 'uk', 'Великобритания'
        FRANCE = 'france', 'Франция'
        ITALY = 'italy', 'Италия'
        CHINA = 'china', 'Китай'
        JAPAN = 'japan', 'Япония'
        POLAND = 'poland', 'Польша'
        SWEDEN = 'sweden', 'Швеция'
        CZECH = 'czech', 'Чехословакия'

    name = models.CharField(max_length=256)
    level = models.PositiveSmallIntegerField()
    type = models.CharField(max_length=10, choices=Type)
    nation = models.CharField(max_length=7, choices=Nation)
    contour = models.ImageField(upload_to='tanks/', storage=OverWriteStorage())

    def __str__(self) -> str:
        return f'{self.name} ({self.level} lvl.)'
