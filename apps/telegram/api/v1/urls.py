from django.urls import path

from apps.telegram.api.v1.views.telegram import TelegramLoginView, TelegramView

urlpatterns = [
    path('', TelegramView.as_view()),
    path('<int:user_id>/login/', TelegramLoginView.as_view()),
]
