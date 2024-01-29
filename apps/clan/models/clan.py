from django.db import models

from mixins.models import DateTimeMixin, ExternalIDMixin


class Clan(DateTimeMixin, ExternalIDMixin):
    tag = models.CharField(max_length=5)
    name = models.CharField(max_length=128)
    motto = models.TextField()
    color = models.CharField(max_length=7)
    emblem = models.URLField()

    def __str__(self) -> str:
        return f'[{self.tag}] {self.name}'
