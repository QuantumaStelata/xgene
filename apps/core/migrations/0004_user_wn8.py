# Generated by Django 5.0 on 2024-02-16 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_user_battles_user_bonds_user_credits_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='wn8',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
