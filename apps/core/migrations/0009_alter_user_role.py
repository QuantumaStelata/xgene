# Generated by Django 5.0 on 2024-05-02 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_user_external_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.IntegerField(choices=[(1, 'Командующий'), (2, 'Заместитель командующего'), (3, 'Офицер штаба'), (4, 'Командир подразделения'), (5, 'Офицер разведки'), (6, 'Офицер снабжения'), (7, 'Офицер по кадрам'), (8, 'Младший офицер'), (9, 'Боец'), (10, 'Новобранец'), (11, 'Резервист')], help_text='Роль'),
        ),
    ]