# Generated by Django 5.0 on 2024-05-06 19:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clan', '0005_alter_clan_options_alter_stronghold_options_and_more'),
        ('directory', '0015_auto_20240506_2208'),
    ]

    operations = [
        migrations.AddField(
            model_name='build',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='builds', to='directory.strongholdbuildtype'),
        ),
    ]
