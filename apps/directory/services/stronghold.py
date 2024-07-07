import json

from apps.directory.models import StrongholdBuildType


class StrongholdBuildTypeService:
    @classmethod
    def update_build_types(cls) -> list[StrongholdBuildType]:
        fixture = 'fixtures/stronghold_build_types.json'

        build_types = []
        data = None
        with open(fixture, encoding='utf-8') as file:
            data = json.load(file)

        if not data:
            return []

        for build_type in data:
            build_types.append(StrongholdBuildType(**build_type))

        return StrongholdBuildType.objects.bulk_create(
            build_types,
            update_conflicts=True,
            update_fields=['name', 'name_en', 'name_ru', 'external_id'],
            unique_fields=['id'],
        )
