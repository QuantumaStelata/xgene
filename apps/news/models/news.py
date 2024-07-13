from django.db import models

from generic.storages import OverWriteStorage
from mixins.models import DateTimeMixin, ExternalStrIDMixin


class New(DateTimeMixin, ExternalStrIDMixin):
    category = models.ForeignKey('news.NewCategory', on_delete=models.CASCADE, related_name='news')
    title = models.TextField()
    description = models.TextField()
    image = models.ImageField(upload_to='news/', storage=OverWriteStorage())
    link = models.URLField()
    pub_date = models.DateTimeField()

    class Meta:
        ordering = ('-pub_date',)
