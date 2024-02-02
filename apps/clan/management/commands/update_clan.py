from django.core.management.base import BaseCommand, CommandError

from apps.clan.services.clan import ClanService


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            ClanService.update_clan()
        except Exception as e:
            raise CommandError('Load clan error') from e
