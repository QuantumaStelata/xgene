import enum

from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from apps.clan.models import Reserve
from apps.core.services.login import LoginService
from apps.directory.models import Role
from apps.integrations.telegram.models import TelegramUser
from generic.utils import concat_path_to_domain


class MessageCallBack(str, enum.Enum):
    BACK_TO_MAIN = 'back_to_main'

    MY_STATISTICS = 'my_statistics'
    ACTIVATE_RESERVES = 'acticate_reservers'
    ACTIVATE_RESERVE = 'activate_reserve'
    ACTIVATE_RESERVE_TEMPLATE = f'{ACTIVATE_RESERVE}:%s'


class TelegramMessageGeneric:
    text: str = None
    parse_mode: str = 'Markdown'
    bot = TeleBot(settings.TELEGRAM_API_KEY)

    @classmethod
    def get_text(cls, user: TelegramUser | int, *args, **kwargs) -> str:
        return str(cls.text)

    @classmethod
    def get_markup(cls, user: TelegramUser | int, *args, **kwargs) -> None:
        return None

    @classmethod
    def get_chat_id(cls, user: TelegramUser | int, *args, **kwargs) -> int:
        if isinstance(user, TelegramUser):
            return user.external_id
        return user

    @classmethod
    def send(cls, user: TelegramUser | int, *args, **kwargs) -> Message:
        chat_id = cls.get_chat_id(user=user, *args, **kwargs)
        text = cls.get_text(user=user, *args, **kwargs)
        markup = cls.get_markup(user=user, *args, **kwargs)

        return cls.bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=markup,
            parse_mode=cls.parse_mode,
        )


class ErrorMessage(TelegramMessageGeneric):
    text = _('An error occurred, please try again later')


class AuthMessage(TelegramMessageGeneric):
    text = _('Log in via WG OpenID using the [link](%(link)s)')

    @classmethod
    def get_text(cls, user: TelegramUser | int, *args, **kwargs) -> str:
        if isinstance(user, TelegramUser):
            user = user.external_id

        redirect_uri = concat_path_to_domain(reverse('telegram:login', kwargs={'user_id': user}))
        link = LoginService.get_openid_url(redirect_uri=redirect_uri)
        return super().get_text(user, *args, **kwargs) % {'link': link}


class MainMessage(TelegramMessageGeneric):
    text = _('Hello, %(username)s!')

    @classmethod
    def get_text(cls, user: TelegramUser | int, *args, **kwargs) -> str:
        return super().get_text(user, *args, **kwargs) % {'username': user.user.username}

    @classmethod
    def get_markup(cls, user: TelegramUser | int, *args, **kwargs) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text=str(_('My statistics')), callback_data=MessageCallBack.MY_STATISTICS))

        if user.user.role_id in {
            Role.PrimaryID.COMMANDER,
            Role.PrimaryID.EXECUTIVE_OFFICER,
            Role.PrimaryID.PERSONNEL_OFFICER,

        }:
            markup.add(
                InlineKeyboardButton(text=str(_('Activate reserves')), callback_data=MessageCallBack.ACTIVATE_RESERVES),
            )

        return markup


class MyStatisticsMessage(TelegramMessageGeneric):
    text = _(
        'My statistics:\n\nBattles: %(battles)s\nWinrate: %(wins_percent)s%%\nWN8: %(wn8)s\n\n'
        'Max damage: %(max_damage)s (%(max_damage_tank)s)\nMax frags: %(max_frags)s (%(max_frags_tank)s)',
    )

    @classmethod
    def get_text(cls, user: TelegramUser | int, *args, **kwargs) -> str:
        return super().get_text(user, *args, **kwargs) % {
            'battles': user.user.battles,
            'wins_percent': user.user.wins_percent,
            'wn8': user.user.wn8,
            'max_damage': user.user.max_damage,
            'max_frags': user.user.max_frags,
            'max_damage_tank': user.user.max_damage_tank.name,
            'max_frags_tank': user.user.max_frags_tank.name,
        }

    @classmethod
    def get_markup(cls, user: TelegramUser | int, *args, **kwargs) -> None:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text=str(_('Back')), callback_data=MessageCallBack.BACK_TO_MAIN))
        return markup


class ActivateReservesMessage(TelegramMessageGeneric):
    text = _('Which reserve should be activated?')

    @classmethod
    def get_markup(cls, user: TelegramUser | int, *args, **kwargs) -> None:
        markup = InlineKeyboardMarkup()

        reserves = Reserve.objects.select_related('type').filter(
            ready_to_activate=True, disposable=False,
        ).order_by('-level')

        for reserve in reserves:
            text = str(_('%(name)s, %(level)s lvl (%(count)s pieces)')) % {
                'name': reserve.type.name,
                'level': reserve.level,
                'count': reserve.count,
            }
            callback_data = MessageCallBack.ACTIVATE_RESERVE_TEMPLATE % reserve.id
            markup.add(InlineKeyboardButton(text=text, callback_data=callback_data))
        markup.add(InlineKeyboardButton(text=str(_('Back')), callback_data=MessageCallBack.BACK_TO_MAIN))
        return markup


class ReserveSuccessfullyActivatedMessage(TelegramMessageGeneric):
    text = _('The reserve has been successfully activated!')


class ReserveActivatedMessage(TelegramMessageGeneric):
    text = _('Enter the game, the "%(reserve_name)s" reserve is activated!')

    @classmethod
    def get_text(cls, user: TelegramUser | int, reserve: Reserve, *args, **kwargs) -> str:  # pylint: disable=W0221
        return super().get_text(user, *args, **kwargs) % {'reserve_name': reserve.type.name}
