# Generated by Django 5.0 on 2024-05-07 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0018_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='name_en',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='role',
            name='name_ru',
            field=models.CharField(max_length=64, null=True),
        ),
    ]