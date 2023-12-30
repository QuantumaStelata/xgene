from django.db import models


class Player(models.Model):
    class Role(models.IntegerChoices):
        COMMANDER = 1, 'Командующий'
        EXECUTIVE_OFFICER = 2, 'Заместитель командующего'
        PERSONNEL_OFFICER = 3, 'Офицер штаба'
        # Ком подразделения
        # Оф снабжения
        RECRUITMENT_OFFICER = 6, 'Офицер по кадрам'
        JUNIOR_OFFICER = 7, 'Младший офицер'
        PRIVATE = 8, 'Боец'
        RECRUIT = 9, 'Новобранец'
        RESERVIST = 10, 'Резервист'

    ROLE_MAP = {
        'commander': Role.COMMANDER,
        'executive_officer': Role.EXECUTIVE_OFFICER,
        'personnel_officer': Role.PERSONNEL_OFFICER,
        'recruitment_officer': Role.RECRUITMENT_OFFICER,
        'junior_officer': Role.JUNIOR_OFFICER,
        'private': Role.PRIVATE,
        'recruit': Role.RECRUIT,
        'reservist': Role.RESERVIST,
    }

    name = models.CharField(max_length=256)
    role = models.IntegerField()
    account_id = models.IntegerField(unique=True)
