# Generated by Django 5.0 on 2024-02-01 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tank',
            name='level',
            field=models.PositiveSmallIntegerField(),
        ),
    ]