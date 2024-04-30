# Generated by Django 5.0 on 2024-02-10 21:50

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tactic', '0002_room_users'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='users',
        ),
        migrations.CreateModel(
            name='UserRoomRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'Admin'), (2, 'General')], default=2)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='tactic.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at', '-modified_at'],
                'abstract': False,
            },
        ),
    ]