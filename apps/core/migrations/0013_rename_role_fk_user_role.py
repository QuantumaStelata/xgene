# Generated by Django 5.0 on 2024-05-07 22:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_remove_user_role'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='role_fk',
            new_name='role',
        ),
    ]
