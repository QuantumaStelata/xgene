import contextlib
from datetime import timedelta

from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import activate
from telebot import TeleBot
from telebot.types import CallbackQuery, Message, Update

from apps.clan.models import Reserve
from apps.clan.services.reserve import ReserveService
from apps.core.services.login import LoginService
from apps.integrations.telegram.api.v1.services.messages import (
    ActivateReservesMessage, AuthMessage, ErrorMessage, MainMessage, MessageCallBack, MyStatisticsMessage,
    ReserveActivatedMessage, ReserveSuccessfullyActivatedMessage,
)
from apps.integrations.telegram.models import TelegramUser
from generic.utils import concat_path_to_domain


class TelegramService:
    bot = TeleBot(settings.TELEGRAM_API_KEY)

    @classmethod
    def setup(cls):
        if not settings.TELEGRAM_API_KEY:
            return

        cls.bot.delete_webhook()
        cls.bot.delete_my_commands()

        url = concat_path_to_domain(reverse('telegram:webhook'))
        cls.bot.set_webhook(url=url, secret_token=settings.TELEGRAM_API_SECRET)

    @classmethod
    def webhook(cls, data: dict):
        if not settings.TELEGRAM_API_KEY:
            return

        update: Update = Update.de_json(data)
        detail = cls.get_detail(update)

        if not detail:
            return

        language = cls.validate_language(detail.from_user.language_code)
        activate(language)

        try:
            user, _ = TelegramUser.objects.select_related('user').update_or_create(
                external_id=detail.from_user.id, defaults={'language': language},
            )
        except TelegramUser.DoesNotExist:
            return AuthMessage.send(bot=cls.bot, user=detail.from_user.id)

        if isinstance(detail, CallbackQuery):
            return cls.proccess_callback(detail, user)
        return MainMessage.send(bot=cls.bot, user=user)

    @classmethod
    def get_detail(cls, update: Update) -> Message | CallbackQuery | None:
        if update.message:
            return update.message
        if update.callback_query:
            return update.callback_query

    @classmethod
    def validate_language(cls, language: str) -> str:
        if language.lower().strip() not in settings.MODELTRANSLATION_LANGUAGES:
            language = settings.MODELTRANSLATION_DEFAULT_LANGUAGE

        return language

    @classmethod
    def proccess_callback(cls, callback: CallbackQuery, user: TelegramUser):
        message = None

        match callback.data.split(':'):
            case MessageCallBack.BACK_TO_MAIN, *_:
                message = MainMessage
            case MessageCallBack.MY_STATISTICS, *_:
                message = MyStatisticsMessage
            case MessageCallBack.ACTIVATE_RESERVES, *_:
                message = ActivateReservesMessage
            case MessageCallBack.ACTIVATE_RESERVE, str() as reserve_id:
                with contextlib.suppress(Reserve.DoesNotExist):
                    reserve = Reserve.objects.get(id=reserve_id)
                    if ReserveService.activate_reserve(user=user.user, reserve=reserve):
                        message = ReserveSuccessfullyActivatedMessage

        if not message:
            message = ErrorMessage

        return message.send(user=user)

    @classmethod
    def send_message(cls, user: int | TelegramUser, **options):
        if not settings.TELEGRAM_API_KEY:
            return

        if isinstance(user, TelegramUser):
            user = user.external_id

        options['chat_id'] = user
        return cls.bot.send_message(**options)

    @classmethod
    def auth(cls, user_id: int, username: str, access_token: str, external_id: int):
        if not settings.TELEGRAM_API_KEY:
            return

        token = LoginService.login(
            username=username,
            access_token=access_token,
            external_id=external_id,
        )

        if not token:
            return ErrorMessage.send(bot=cls.bot, user=external_id)

        user, _ = TelegramUser.objects.get_or_create(user=token.user, external_id=user_id)
        return MainMessage.send(bot=cls.bot, user=user)

    @classmethod
    def reserve_activated_message(cls, delta: int = 5):
        now = timezone.now()
        users = TelegramUser.objects.all()
        reserves = Reserve.objects.select_related('type').filter(
            active_till__gt=now,
            activated_at__range=(now - timedelta(minutes=delta), now),
        )

        if reserves:
            for user in users:
                activate(user.language)

                for reserve in reserves:
                    ReserveActivatedMessage.send(user=user, reserve=reserve)
