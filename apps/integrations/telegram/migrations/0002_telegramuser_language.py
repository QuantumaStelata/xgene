# Generated by Django 5.0.7 on 2024-09-10 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='language',
            field=models.CharField(default='en', max_length=2),
        ),
    ]
