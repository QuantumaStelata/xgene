import json

from django.core.files.base import ContentFile

from apps.directory.models import Map


class MapService:
    @classmethod
    def update_maps(cls) -> list[Map]:
        fixture = 'fixtures/maps.json'

        maps = []
        data = None
        with open(fixture, encoding='utf-8') as file:
            data = json.load(file)

        if not data:
            return []

        for _map in data:
            file_path = _map['file']
            with open(file_path, 'rb') as file:
                _map['file'] = ContentFile(file.read(), name=file_path.rsplit('/', maxsplit=1)[-1])

            maps.append(Map(**_map))

        return Map.objects.bulk_create(
            maps,
            update_conflicts=True,
            update_fields=['name', 'name_en', 'name_ru', 'file', 'external_id'],
            unique_fields=['id'],
        )
