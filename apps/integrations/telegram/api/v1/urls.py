from django.urls import path

from apps.integrations.telegram.api.v1.views.telegram import TelegramLoginView, TelegramWebhookViewSet

app_name = 'telegram'

urlpatterns = [
    path('webhook/', TelegramWebhookViewSet.as_view(), name='webhook'),
    path('<int:user_id>/login/', TelegramLoginView.as_view(), name='login'),
]
