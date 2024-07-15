from django.db import models

from mixins.models import AuthorMixin, DateTimeMixin


class Reaction(AuthorMixin, DateTimeMixin):
    class Type(models.IntegerChoices):
        LIKE = 1
        DISLIKE = 2

    new = models.ForeignKey('news.New', on_delete=models.CASCADE, related_name='reactions')
    type = models.PositiveSmallIntegerField(choices=Type)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['new', 'author'],
                name='new and author unique constraint',
            ),
        ]
