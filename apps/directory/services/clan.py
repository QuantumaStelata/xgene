import json

from apps.directory.models import Role


class RoleService:
    @classmethod
    def update_roles(cls) -> list[Role]:
        fixture = 'fixtures/clan_roles.json'

        build_types = []
        data = None
        with open(fixture, encoding='utf-8') as file:
            data = json.load(file)

        if not data:
            return []

        for build_type in data:
            build_types.append(Role(**build_type))

        return Role.objects.bulk_create(
            build_types,
            update_conflicts=True,
            update_fields=['name', 'name_en', 'name_ru', 'external_id'],
            unique_fields=['id'],
        )
