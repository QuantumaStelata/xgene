from django.db import models

from mixins.models import DateTimeMixin


class NewCategory(DateTimeMixin):
    name = models.CharField(max_length=128)
