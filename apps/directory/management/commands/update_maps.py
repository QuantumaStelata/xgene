from django.core.management.base import BaseCommand, CommandError

from apps.directory.services.maps import MapService


class Command(BaseCommand):
    def handle(self, *args, **options):
        maps = MapService.update_maps()

        if not maps:
            raise CommandError('Fixture read error')
