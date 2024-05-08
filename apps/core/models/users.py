from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F, Value

from mixins.models import DateTimeMixin, ExternalIDMixin


class User(DateTimeMixin, ExternalIDMixin, AbstractUser):
    first_name = None
    last_name = None
    email = None

    role = models.ForeignKey('directory.Role', on_delete=models.CASCADE, null=True, related_name='users')
    access_token = models.CharField(max_length=40, blank=True)

    credits = models.PositiveIntegerField(null=True)
    bonds = models.PositiveIntegerField(null=True)
    gold = models.PositiveIntegerField(null=True)
    free_xp = models.PositiveIntegerField(null=True)

    battles = models.PositiveIntegerField(null=True)
    wins = models.PositiveIntegerField(null=True)
    draws = models.PositiveIntegerField(null=True)
    losses = models.PositiveIntegerField(null=True)

    max_damage = models.PositiveIntegerField(null=True)
    max_frags = models.PositiveIntegerField(null=True)
    max_xp = models.PositiveIntegerField(null=True)
    max_damage_tank = models.ForeignKey(
        'directory.Tank', on_delete=models.SET_NULL, null=True, related_name='max_damage_users',
    )
    max_frags_tank = models.ForeignKey(
        'directory.Tank', on_delete=models.SET_NULL, null=True, related_name='max_frags_users',
    )
    max_xp_tank = models.ForeignKey(
        'directory.Tank', on_delete=models.SET_NULL, null=True, related_name='max_xp_users',
    )

    frags = models.PositiveIntegerField(null=True)
    spotted = models.PositiveIntegerField(null=True)
    dropped_capture_points = models.PositiveIntegerField(null=True)
    damage_dealt = models.PositiveIntegerField(null=True)
    damage_received = models.PositiveIntegerField(null=True)

    shots = models.PositiveIntegerField(null=True)
    hits = models.PositiveIntegerField(null=True)

    wins_percent = models.GeneratedField(
        expression=F('wins') * Value(100) / F('battles'),
        output_field=models.FloatField(),
        db_persist=True,
    )
    hits_percent = models.GeneratedField(
        expression=F('hits') * Value(100) / F('shots'),
        output_field=models.FloatField(),
        db_persist=True,
    )

    wn8 = models.PositiveIntegerField(null=True)

    def __str__(self) -> str:
        return self.username
