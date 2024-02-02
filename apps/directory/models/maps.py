from django.db import models

from generic.storages import OverWriteStorage
from mixins.models import DateTimeMixin, ExternalStrIDMixin


class Map(DateTimeMixin, ExternalStrIDMixin):
    name = models.CharField(max_length=128)
    file = models.ImageField(upload_to='maps/', storage=OverWriteStorage())
