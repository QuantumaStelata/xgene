# Generated by Django 5.0 on 2024-02-02 22:34

from django.db import migrations


def update_reserve_types(apps, schema_editor):
    # Deprecated
    # from apps.directory.services.reserve_types import ReserveTypeService
    # ReserveTypeService.update_reserve_types()
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0007_reservetype'),
    ]

    operations = [
        migrations.RunPython(update_reserve_types, reverse_code=migrations.RunPython.noop),
    ]
