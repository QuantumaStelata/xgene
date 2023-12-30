from django.db import models


class Clan(models.Model):
    tag = models.CharField(max_length=5)
    name = models.TextField()
    motto = models.TextField()
    color = models.CharField(max_length=7)
    emblem = models.URLField()
    clan_id = models.IntegerField(unique=True)
