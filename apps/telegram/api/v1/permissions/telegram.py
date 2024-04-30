from django.conf import settings
from rest_framework.permissions import BasePermission


class TelegramPermission(BasePermission):
    def has_permission(self, request, view):
        return request.headers.get('X-Telegram-Bot-Api-Secret-Token') == settings.TELEGRAM_API_SECRET
