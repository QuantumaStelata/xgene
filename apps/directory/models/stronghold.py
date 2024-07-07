from django.db import models


class StrongholdBuildType(models.Model):
    class PrimaryID(models.IntegerChoices):
        FINANCIAL_UNIT = 1
        TANKODROME = 2
        MILITARY_SCHOOL = 3
        TRAINING_UNIT = 4
        TRANSPORTATION_UNIT = 5
        TROPHY_BRIGADE = 6
        ARTILLERY_BATTALION = 7
        LOGISTICAL_SERVICE = 8

    class ExternalID(models.TextChoices):
        FINANCIAL_UNIT = 'Financial Unit'
        TANKODROME = 'Tankodrome'
        MILITARY_SCHOOL = 'Military School'
        TRAINING_UNIT = 'Training Unit'
        TRANSPORTATION_UNIT = 'Transportation Unit'
        TROPHY_BRIGADE = 'Trophy Brigade'
        ARTILLERY_BATTALION = 'Artillery Battalion'
        LOGISTICAL_SERVICE = 'Logistical Service'

    name = models.CharField(max_length=64)
    external_id = models.CharField(max_length=32, choices=ExternalID, unique=True)
