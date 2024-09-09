from apps.integrations.telegram.api.v1.services.telegram import TelegramService
from cluster import celery_app


@celery_app.task(priority=1)
def telegram_webhook(data: dict):
    TelegramService.webhook(data)
