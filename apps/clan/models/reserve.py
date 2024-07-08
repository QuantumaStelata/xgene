from django.db import models

from mixins.models import AuthorMixin, DateTimeMixin


class Reserve(DateTimeMixin):
    type = models.ForeignKey('directory.ReserveType', on_delete=models.CASCADE, related_name='reserves')
    level = models.PositiveSmallIntegerField()
    count = models.PositiveSmallIntegerField()
    clan_bonus = models.FloatField(null=True)
    random_bonus = models.FloatField(null=True)
    activated_at = models.DateTimeField(null=True)
    active_till = models.DateTimeField(null=True)
    disposable = models.BooleanField(default=False, help_text='Является ли резерв резервом для сражений')
    ready_to_activate = models.BooleanField(default=False)
    x_level_only = models.BooleanField(default=False)

    class Meta:
        ordering = ['type', 'level']
        constraints = [
            models.UniqueConstraint(
                fields=['type', 'level'],
                name='type and level unique constraint',
            ),
        ]


class ReserveScheduler(AuthorMixin, DateTimeMixin):
    class Day(models.IntegerChoices):
        MONDAY = 0
        TUESDAY = 1
        WEDNESDAY = 2
        THURSDAY = 3
        FRIDAY = 4
        SATURDAY = 5
        SUNDAY = 6

    reserve = models.ForeignKey(
        'clan.Reserve',
        on_delete=models.CASCADE,
        related_name='schedulers',
        limit_choices_to={'disposable': False},
    )
    day = models.PositiveSmallIntegerField(choices=Day)
    time = models.TimeField()
