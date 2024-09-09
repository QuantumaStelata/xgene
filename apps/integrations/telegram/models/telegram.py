from django.db import models

from mixins.models import DateTimeMixin, ExternalIDMixin


class TelegramUser(DateTimeMixin, ExternalIDMixin):
    user = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='telegram_users')
