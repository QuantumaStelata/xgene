from django.contrib.auth.models import AbstractUser
from django.db import models

from mixins.models import DateTimeMixin, ExternalIDMixin


class User(DateTimeMixin, ExternalIDMixin, AbstractUser):
    first_name = None
    last_name = None
    email = None

    class Role(models.IntegerChoices):
        COMMANDER = 1, 'Командующий'
        EXECUTIVE_OFFICER = 2, 'Заместитель командующего'
        PERSONNEL_OFFICER = 3, 'Офицер штаба'
        COMBAT_OFFICER = 4, 'Командир подразделения'
        QUARTERMASTER = 5, 'Офицер снабжения'
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
        'combat_officer': Role.COMBAT_OFFICER,
        'quartermaster': Role.QUARTERMASTER,
        'junior_officer': Role.JUNIOR_OFFICER,
        'private': Role.PRIVATE,
        'recruit': Role.RECRUIT,
        'reservist': Role.RESERVIST,
    }

    role = models.IntegerField(choices=Role, help_text='Роль')
    access_token = models.CharField(max_length=40, blank=True)

    def __str__(self) -> str:
        return self.username
