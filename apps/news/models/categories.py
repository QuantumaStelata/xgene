from django.db import models

from mixins.models import DateTimeMixin


class Category(DateTimeMixin):
    name = models.CharField(max_length=128)
