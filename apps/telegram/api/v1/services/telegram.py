import enum

from django.conf import settings
from telebot import TeleBot
from telebot.formatting import hlink
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, Message

from apps.clan.models import Reserve
from apps.clan.services.reserve import ReserveService
from apps.core.models import User
from apps.core.services.login import LoginService
from apps.telegram.models import TelegramUser


class MessageCommand(str, enum.Enum):
    RESERVE_ON = 'Включить плюху'
    BACK = 'Назад'


class TelegramService:
    bot = TeleBot(settings.TELEGRAM_API_KEY)

    @classmethod
    def parse_message(cls, data: dict):
        message: Message = Message.de_json(data)
        print(message)

        try:
            user = TelegramUser.objects.select_related('user').get(external_id=message.from_user.id).user
        except TelegramUser.DoesNotExist:
            return cls.message_auth(message.from_user.id)

        try:
            match message.text:
                case MessageCommand.RESERVE_ON:
                    cls.message_reserve(user)
                case _:
                    cls.message_main(user)
        except Exception as e:
            print(e)

    @classmethod
    def auth(cls, user_id: int, username: str, access_token: str, external_id: int):
        token = LoginService.login(
            username=username,
            access_token=access_token,
            external_id=external_id,
        )

        if not token:
            return cls.send_message(user_id, text='Не удалось авторизоваться')

        TelegramUser.objects.get_or_create(user=token.user, external_id=user_id)
        cls.message_main(token.user)

    @classmethod
    def message_auth(cls, user_id: int):
        redirect_uri = f'{settings.BACK_DOMAIN}api/v1/telegram/{user_id}/login/'
        url = LoginService.get_openid_url(redirect_uri=redirect_uri)
        cls.send_message(user_id, text=f'Авторизируйтесь через WG OpenID по {hlink("ссылке", url)}', parse_mode='html')

    @classmethod
    def message_main(cls, user: User):
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(MessageCommand.RESERVE_ON, callback_data='reserve_on')
        markup.add(button_1)
        cls.send_message(user, text=f'Привет, {user.username}!', reply_markup=markup)

    @classmethod
    def message_reserve(cls, user: User):
        ReserveService.update_reserves()
        reserves = Reserve.objects.select_related('type').filter(ready_to_activate=True, disposable=False)
        reserves_text = '\n'.join([f'{str(i)}) {reserve.type.name}' for i, reserve in enumerate(reserves, 1)])
        text = f'Клановые резервы:\n\n{reserves_text}'
        markup = InlineKeyboardMarkup()
        for reserve in reserves:
            button = InlineKeyboardButton(
                f'{reserve.type.name} | Уровень {reserve.level} | Всего {reserve.count}',
                callback_data=f'activate_reserve_{reserve.id}',
            )
            markup.add(button)
        button = KeyboardButton(MessageCommand.BACK)
        markup.add(button)
        cls.send_message(user, text=text, reply_markup=markup)

    @classmethod
    def send_message(cls, user: int | TelegramUser | User, **options):
        if isinstance(user, TelegramUser):
            user = user.external_id
        elif isinstance(user, User):
            user = user.telegram_user.external_id

        options['chat_id'] = user
        return cls.bot.send_message(**options)
