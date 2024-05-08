from django.db import models


class Role(models.Model):
    class PrimaryID(models.IntegerChoices):
        COMMANDER = 1
        EXECUTIVE_OFFICER = 2
        PERSONNEL_OFFICER = 3
        COMBAT_OFFICER = 4
        INTELLIGENCE_OFFICER = 5
        QUARTERMASTER = 6
        RECRUITMENT_OFFICER = 7
        JUNIOR_OFFICER = 8
        PRIVATE = 9
        RECRUIT = 10
        RESERVIST = 11

    class ExternalID(models.TextChoices):
        COMMANDER = 'commander'
        EXECUTIVE_OFFICER = 'executive_officer'
        PERSONNEL_OFFICER = 'personnel_officer'
        COMBAT_OFFICER = 'combat_officer'
        INTELLIGENCE_OFFICER = 'intelligence_officer'
        QUARTERMASTER = 'quartermaster'
        RECRUITMENT_OFFICER = 'recruitment_officer'
        JUNIOR_OFFICER = 'junior_officer'
        PRIVATE = 'private'
        RECRUIT = 'recruit'
        RESERVIST = 'reservist'

    name = models.CharField(max_length=64)
    external_id = models.CharField(max_length=32, choices=ExternalID, unique=True)
