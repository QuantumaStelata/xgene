from apps.integrations.telegram.api.v1.services.telegram import TelegramService
from apps.integrations.telegram.models import TelegramUser
from cluster import celery_app


@celery_app.task(priority=1)
def telegram_webhook(data: dict):
    TelegramService.webhook(data)


@celery_app.task(serializer='pickle')
def telegram_send(user: TelegramUser, **options):
    TelegramService.send_message(user=user, **options)


@celery_app.task()
def reserve_activated_message():
    TelegramService.reserve_activated_message()
