from django.db import models

from mixins.models import AuthorMixin, DateTimeMixin


class Comment(DateTimeMixin, AuthorMixin):
    new = models.ForeignKey('news.New', on_delete=models.CASCADE, related_name='comments')
    text = models.CharField(max_length=1024)
