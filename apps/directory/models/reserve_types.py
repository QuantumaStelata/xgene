from django.db import models

from generic.storages import OverWriteStorage


class ReserveType(models.Model):
    class ExternalID(models.TextChoices):
        BATTLE_PAYMENTS = 'BATTLE_PAYMENTS', 'Боевые выплаты'
        TACTICAL_TRAINING = 'TACTICAL_TRAINING', 'Тактическая подготовка'
        MILITARY_MANEUVERS = 'MILITARY_MANEUVERS', 'Военные учения'
        ADDITIONAL_BRIEFING = 'ADDITIONAL_BRIEFING', 'Дополнительный инструктаж'
        HIGH_CAPACITY_TRANSPORT = 'HIGH_CAPACITY_TRANSPORT', 'Большегрузный транспорт'
        REQUISITION = 'REQUISITION', 'Реквизиция'
        ARTILLERY_STRIKE = 'ARTILLERY_STRIKE', 'Артобстрел'
        INSPIRATION = 'INSPIRATION', 'Воодушевление'

    name = models.CharField(max_length=128)
    file = models.ImageField(upload_to='reserve_types/', storage=OverWriteStorage())
    external_id = models.CharField(max_length=32, choices=ExternalID, unique=True)
