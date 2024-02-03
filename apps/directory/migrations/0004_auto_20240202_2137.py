# Generated by Django 5.0 on 2024-02-02 19:37

from django.db import migrations


def update_maps(apps, schema_editor):
    from apps.directory.services.maps import MapService
    MapService.update_maps()


class Migration(migrations.Migration):
    dependencies = [
        ('directory', '0003_map'),
    ]

    operations = [
        migrations.RunPython(update_maps, reverse_code=migrations.RunPython.noop),
    ]