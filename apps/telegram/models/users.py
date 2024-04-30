from django.db import models

from mixins.models import ExternalIDMixin


class TelegramUser(ExternalIDMixin):
    user = models.OneToOneField('core.User', on_delete=models.CASCADE, related_name='telegram_user')
