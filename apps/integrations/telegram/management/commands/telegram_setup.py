from django.core.management.base import BaseCommand

from apps.integrations.telegram.api.v1.services.telegram import TelegramService


class Command(BaseCommand):
    def handle(self, *args, **options):
        TelegramService.setup()
