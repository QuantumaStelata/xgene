# Generated by Django 5.0 on 2024-05-06 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0013_strongholdbuildtype'),
    ]

    operations = [
        migrations.AddField(
            model_name='strongholdbuildtype',
            name='name_en',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='strongholdbuildtype',
            name='name_ru',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
