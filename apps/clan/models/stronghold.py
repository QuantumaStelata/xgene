from django.db import models

from mixins.models import DateTimeMixin


class Stronghold(DateTimeMixin):
    clan = models.OneToOneField('clan.Clan', on_delete=models.CASCADE, related_name='stronghold')
    level = models.PositiveSmallIntegerField()
    map = models.ForeignKey('directory.Map', on_delete=models.SET_NULL, null=True)


class Build(DateTimeMixin):
    class Title(models.TextChoices):
        FINANCIAL_UNIT = 'Financial Unit', 'Финансовая часть'
        TANKODROME = 'Tankodrome', 'Танкодром'
        MILITARY_SCHOOL = 'Military School', 'Военное училище'
        TRAINING_UNIT = 'Training Unit', 'Учебная часть'
        TRANSPORTATION_UNIT = 'Transportation Unit', 'Автотранспортная часть'
        TROPHY_BRIGADE = 'Trophy Brigade', 'Трофейная бригата'
        ARTILLERY_BATTALION = 'Artillery Battalion', 'Артиллерийский дивизион'
        LOGISTICAL_SERVICE = 'Logistical Service', 'Служба тыла'

    class Direction(models.TextChoices):
        A = 'A'
        B = 'B'
        C = 'C'
        D = 'D'

    class Position(models.IntegerChoices):
        P1 = 1
        P2 = 2

    stronghold = models.ForeignKey('clan.Stronghold', on_delete=models.CASCADE, related_name='builds')
    title = models.CharField(max_length=32, choices=Title)
    direction = models.CharField(max_length=32, choices=Direction)
    position = models.PositiveSmallIntegerField(choices=Position)
    level = models.PositiveSmallIntegerField()
    map = models.ForeignKey('directory.Map', on_delete=models.SET_NULL, null=True)
    reserve_type = models.ForeignKey(
        'directory.ReserveType', on_delete=models.SET_NULL, null=True, related_name='build',
    )

    class Meta:
        ordering = ['direction', 'position']
        constraints = [
            models.UniqueConstraint(
                fields=['stronghold', 'direction', 'position'],
                name='stronghold, direction and position unique constraint',
            ),
            models.UniqueConstraint(
                fields=['stronghold', 'title'],
                name='stronghold and title unique constraint',
            ),
            models.UniqueConstraint(
                fields=['stronghold', 'reserve_type'],
                name='stronghold and reserve_type unique constraint',
            ),
        ]
