import json

from django.core.files.base import ContentFile

from apps.directory.models import ReserveType


class ReserveTypeService:
    @classmethod
    def update_reserve_types(cls) -> list[ReserveType]:
        fixture = 'fixtures/reserve_types.json'

        reserve_types = []
        data = None
        with open(fixture, encoding='utf-8') as file:
            data = json.load(file)

        if not data:
            return []

        for reserve_type in data:
            file_path = reserve_type['file']
            with open(file_path, 'rb') as file:
                reserve_type['file'] = ContentFile(file.read(), name=file_path.rsplit('/', maxsplit=1)[-1])

            reserve_types.append(ReserveType(**reserve_type))

        return ReserveType.objects.bulk_create(
            reserve_types,
            update_conflicts=True,
            update_fields=['name', 'file'],
            unique_fields=['external_id'],
        )
