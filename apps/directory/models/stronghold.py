from django.db import models


class StrongholdBuildType(models.Model):
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
