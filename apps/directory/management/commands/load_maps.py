import json

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError

from apps.directory.models import Map


class Command(BaseCommand):
    def handle(self, *args, **options):
        fixture = 'fixtures/maps.json'

        maps = []
        data = None
        with open(fixture, encoding='utf-8') as file:
            data = json.load(file)

        if not data:
            raise CommandError('Fixture read error')

        for _map in data:
            file_path = _map['file']
            with open(file_path, 'rb') as file:
                _map['file'] = ContentFile(file.read(), name=file_path.rsplit('/', maxsplit=1)[-1])

            maps.append(Map(**_map))

        Map.objects.bulk_create(
            maps,
            update_conflicts=True,
            update_fields=['name', 'file'],
            unique_fields=['external_id'],
        )
