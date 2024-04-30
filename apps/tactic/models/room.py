import uuid

from django.db import models

from mixins.models import AuthorMixin, DateTimeMixin, SoftDeletionMixin


class Room(SoftDeletionMixin, DateTimeMixin, AuthorMixin):
    uuid = models.UUIDField(default=uuid.uuid4)
    map = models.ForeignKey('directory.Map', on_delete=models.SET_NULL, null=True, related_name='rooms')
    users = models.ManyToManyField('core.User', through='tactic.UserRoomRelation', related_name='rooms')


class UserRoomRelation(DateTimeMixin):
    class Type(models.IntegerChoices):
        ADMIN = 1
        GENERAL = 2

    room = models.ForeignKey('tactic.Room', on_delete=models.CASCADE)
    user = models.ForeignKey('core.User', on_delete=models.CASCADE)
    type = models.PositiveSmallIntegerField(choices=Type, default=Type.GENERAL)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['room', 'user'],
                name='room and user unique together',
                violation_error_code=1,
            ),
        ]

    def save(self, *args, **kwargs):
        if self.room.author_id == self.user_id:
            self.type = self.Type.ADMIN
        super().save(*args, **kwargs)
