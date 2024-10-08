# Generated by Django 5.0 on 2024-04-30 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clan', '0004_alter_clan_emblem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clan',
            options={'ordering': ('-created_at', '-modified_at')},
        ),
        migrations.AlterModelOptions(
            name='stronghold',
            options={'ordering': ('-created_at', '-modified_at')},
        ),
        migrations.AlterField(
            model_name='clan',
            name='external_id',
            field=models.BigIntegerField(unique=True),
        ),
    ]
