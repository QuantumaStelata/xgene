from django.conf import settings
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone

from cluster.middlewares import get_current_authenticated_user


class IsActiveMixin(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class DateTimeMixin(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-modified_at']


class AuthorMixin(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        default=get_current_authenticated_user,
    )

    class Meta:
        abstract = True


class SoftDeletionQuerySet(QuerySet):
    def delete(self):
        return super().update(deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)


class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class SoftDeletionMixin(models.Model):
    deleted_at = models.DateTimeField(null=True, editable=False)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True


class ExternalIDMixin(models.Model):
    external_id = models.IntegerField(unique=True)

    class Meta:
        abstract = True


class ExternalStrIDMixin(models.Model):
    external_id = models.CharField(max_length=128, unique=True)

    class Meta:
        abstract = True
