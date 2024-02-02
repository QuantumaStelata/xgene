import json

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError

from apps.directory.models import Map


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--files-update', type=bool, default=False)

    def handle(self, *args, **options):
        fixture = 'fixtures/maps.json'

        maps = []
        data = None
        with open(fixture, encoding='utf-8') as file:
            data = json.load(file)

        if not data:
            raise CommandError('Fixture read error')

        for _map in data:
            if options.get('files_update'):
                file_path = _map['file']
                with open(file_path, 'rb') as file:
                    _map['file'] = ContentFile(file.read(), name=file_path.rsplit('/', maxsplit=1)[-1])
            else:
                del _map['file']

            maps.append(Map(**_map))

        update_fields = ['name']
        if options.get('files_update'):
            update_fields.append('file')

        Map.objects.bulk_create(
            maps,
            update_conflicts=True,
            update_fields=update_fields,
            unique_fields=['external_id'],
        )
