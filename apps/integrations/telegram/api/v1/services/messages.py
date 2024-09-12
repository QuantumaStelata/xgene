import enum

from django.conf import settings
from django.urls import reverse
from django.utils.translation import activate
from django.utils.translation import gettext_lazy as _
from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from apps.clan.models import Reserve
from apps.clan.services.reserve import ReserveService
from apps.core.models import User
from apps.core.services.core import CoreService
from apps.core.services.login import LoginService
from apps.core.services.users import UserService
from apps.directory.models import Role
from apps.integrations.telegram.models import TelegramUser
from generic.utils import concat_path_to_domain


class MessageCallBack(str, enum.Enum):
    BACK_TO_MAIN = 'back_to_main'

    USER_STATISTICS = 'user_statistics'
    USER_STATISTICS_TEMPLATE = f'{USER_STATISTICS}:%s'
    PAGE_STATISTICS = 'page_statistics'
    PAGE_STATISTICS_TEMPLATE = f'{PAGE_STATISTICS}:%s'

    ACTIVATE_RESERVES = 'acticate_reservers'
    ACTIVATE_RESERVE = 'activate_reserve'
    ACTIVATE_RESERVE_TEMPLATE = f'{ACTIVATE_RESERVE}:%s'


class TelegramMessageGeneric:
    bot = TeleBot(settings.TELEGRAM_API_KEY)

    text: str = None
    parse_mode: str = 'Markdown'

    with_back_button: bool = False

    @classmethod
    def get_text(cls, user: TelegramUser | int, *args, **kwargs) -> str:
        return str(cls.text)

    @classmethod
    def get_markup(cls, user: TelegramUser | int, *args, **kwargs) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup()

    @classmethod
    def get_chat_id(cls, user: TelegramUser | int, *args, **kwargs) -> int:
        if isinstance(user, TelegramUser):
            return user.external_id
        return user

    @classmethod
    def _add_back_button(cls, markup: InlineKeyboardMarkup) -> InlineKeyboardMarkup:
        markup.add(InlineKeyboardButton(text=str(_('Back')), callback_data=MessageCallBack.BACK_TO_MAIN))
        return markup

    @classmethod
    def send(cls, user: TelegramUser | int, *args, **kwargs) -> Message:
        activate(user.language)

        chat_id = cls.get_chat_id(user=user, *args, **kwargs)
        text = cls.get_text(user=user, *args, **kwargs).replace('_', r'\_')
        markup = cls.get_markup(user=user, *args, **kwargs)

        if cls.with_back_button:
            markup = cls._add_back_button(markup=markup)

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
        markup.add(
            InlineKeyboardButton(
                text=str(_('My statistics')),
                callback_data=MessageCallBack.USER_STATISTICS_TEMPLATE % user.user_id,
            ),
        )

        if user.user.role_id in {
            Role.PrimaryID.COMMANDER,
            Role.PrimaryID.EXECUTIVE_OFFICER,
            Role.PrimaryID.PERSONNEL_OFFICER,

        }:
            markup.add(
                InlineKeyboardButton(
                    text=str(_('Activate reserves')),
                    callback_data=MessageCallBack.ACTIVATE_RESERVES,
                ),
            )

        markup.add(
            InlineKeyboardButton(
                text=str(_('Clanmate statistics')),
                callback_data=MessageCallBack.PAGE_STATISTICS_TEMPLATE % 0,
            ),
        )

        return markup


class UserStatisticsMessage(TelegramMessageGeneric):
    text = _(
        "%(username)s's statistics:\n\nBattles: %(battles)s\nWinrate: %(wins_percent)s%%\nWN8: %(wn8)s\n\n"
        'Max damage: %(max_damage)s (%(max_damage_tank)s)\nMax frags: %(max_frags)s (%(max_frags_tank)s)',
    )
    with_back_button = True

    @classmethod
    def get_text(cls, user: TelegramUser | int, requested_user: User, *args, **kwargs) -> str:
        UserService.update_user_stats(user=user.user)

        return super().get_text(user, *args, **kwargs) % {
            'username': requested_user.username,
            'battles': requested_user.battles,
            'wins_percent': requested_user.wins_percent,
            'wn8': requested_user.wn8,
            'max_damage': requested_user.max_damage,
            'max_frags': requested_user.max_frags,
            'max_damage_tank': requested_user.max_damage_tank.name,
            'max_frags_tank': requested_user.max_frags_tank.name,
        }


class PageUserStatisticsMessage(TelegramMessageGeneric):
    text = _('Select a player to view his statistics:')
    with_back_button = True

    @classmethod
    def get_markup(cls, user: TelegramUser | int, page: int, *args, **kwargs) -> None:
        pagination = 5
        queryset_from = page * pagination
        queryset_to = queryset_from + pagination

        if page == 0:
            CoreService.update_users()

        requested_users = User.objects.exclude(id=user.user_id).order_by('role')
        requested_users_count = requested_users.count()

        markup = InlineKeyboardMarkup()
        for requested_user in requested_users[queryset_from:queryset_to]:
            markup.add(
                InlineKeyboardButton(
                    text=requested_user.username,
                    callback_data=MessageCallBack.USER_STATISTICS_TEMPLATE % requested_user.id,
                ),
            )

        additional_buttons = []
        if queryset_from > 0:
            additional_buttons.append(
                InlineKeyboardButton(
                    text='<--',
                    callback_data=MessageCallBack.PAGE_STATISTICS_TEMPLATE % str(page - 1),
                ),
            )
        if queryset_to < requested_users_count:
            additional_buttons.append(
                InlineKeyboardButton(
                    text='-->',
                    callback_data=MessageCallBack.PAGE_STATISTICS_TEMPLATE % str(page + 1),
                ),
            )

        markup.add(*additional_buttons, row_width=len(additional_buttons))
        return markup


class ActivateReservesMessage(TelegramMessageGeneric):
    text = _('Which reserve should be activated?')
    with_back_button = True

    @classmethod
    def get_markup(cls, user: TelegramUser | int, *args, **kwargs) -> None:
        markup = InlineKeyboardMarkup()

        ReserveService.update_reserves()
        CoreService.update_user_access_token(user=user.user)

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
        return markup


class ReserveSuccessfullyActivatedMessage(TelegramMessageGeneric):
    text = _('The reserve has been successfully activated!')


class ReserveActivatedMessage(TelegramMessageGeneric):
    text = _('Enter the game, the "%(reserve_name)s" reserve is activated!')

    @classmethod
    def get_text(cls, user: TelegramUser | int, reserve: Reserve, *args, **kwargs) -> str:  # pylint: disable=W0221
        return super().get_text(user, *args, **kwargs) % {'reserve_name': reserve.type.name}
