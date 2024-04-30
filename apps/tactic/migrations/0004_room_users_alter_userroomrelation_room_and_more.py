# Generated by Django 5.0 on 2024-02-10 22:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tactic', '0003_remove_room_users_userroomrelation'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='users',
            field=models.ManyToManyField(related_name='rooms', through='tactic.UserRoomRelation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userroomrelation',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tactic.room'),
        ),
        migrations.AlterField(
            model_name='userroomrelation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
