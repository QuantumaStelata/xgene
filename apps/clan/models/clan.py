from django.db import models

from generic.storages import OverWriteStorage
from mixins.models import DateTimeMixin, ExternalIDMixin


class Clan(DateTimeMixin, ExternalIDMixin):
    tag = models.CharField(max_length=5)
    name = models.CharField(max_length=128)
    motto = models.TextField()
    color = models.CharField(max_length=7)
    emblem = models.ImageField(upload_to='clan/', storage=OverWriteStorage())

    def __str__(self) -> str:
        return f'[{self.tag}] {self.name}'
