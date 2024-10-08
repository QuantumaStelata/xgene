# Generated by Django 5.0 on 2024-05-07 21:57

from django.db import migrations


def update_roles(apps, schema_editor):
    User = apps.get_model('core.User')
    Role = apps.get_model('directory.Role')

    role_map = {
        1: 'commander',
        2: 'executive_officer',
        3: 'personnel_officer',
        4: 'combat_officer',
        5: 'intelligence_officer',
        6: 'quartermaster',
        7: 'recruitment_officer',
        8: 'junior_officer',
        9: 'private',
        10: 'recruit',
        11: 'reservist',
    }

    users = []
    roles = dict(Role.objects.values_list('external_id', 'id'))
    for user in User.objects.all():
        user.role_fk_id = roles[role_map[user.role]]
        users.append(user)

    User.objects.bulk_update(users, fields=['role_fk_id'])


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_user_role_fk'),
    ]

    operations = [
        migrations.RunPython(update_roles, reverse_code=migrations.RunPython.noop),
    ]
