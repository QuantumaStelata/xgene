from django.db import models

from generic.storages import OverWriteStorage


class ReserveType(models.Model):
    class PrimaryID(models.IntegerChoices):
        BATTLE_PAYMENTS = 1
        TACTICAL_TRAINING = 2
        MILITARY_MANEUVERS = 3
        ADDITIONAL_BRIEFING = 4
        HIGH_CAPACITY_TRANSPORT = 5
        REQUISITION = 6
        ARTILLERY_STRIKE = 7
        INSPIRATION = 8

    class ExternalID(models.TextChoices):
        BATTLE_PAYMENTS = 'BATTLE_PAYMENTS'
        TACTICAL_TRAINING = 'TACTICAL_TRAINING'
        MILITARY_MANEUVERS = 'MILITARY_MANEUVERS'
        ADDITIONAL_BRIEFING = 'ADDITIONAL_BRIEFING'
        HIGH_CAPACITY_TRANSPORT = 'HIGH_CAPACITY_TRANSPORT'
        REQUISITION = 'REQUISITION'
        ARTILLERY_STRIKE = 'ARTILLERY_STRIKE'
        INSPIRATION = 'INSPIRATION'

    name = models.CharField(max_length=128)
    file = models.ImageField(upload_to='reserve_types/', storage=OverWriteStorage())
    external_id = models.CharField(max_length=32, choices=ExternalID, unique=True)
