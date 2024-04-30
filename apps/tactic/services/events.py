import enum


class GeneralEnum(str, enum.Enum):
    def __str__(self):
        return self.value


class Event(GeneralEnum):
    GET_MAP = 'get_map'
    SET_MAP = 'set_map'

    GET_USERS = 'get_users'


class SendTo(GeneralEnum):
    ALL = 'all_users'
    EXCEPT_ME = 'users_except_me'
    ME = 'me'


class Field(GeneralEnum):
    EVENT = 'event'
    MAP = 'map_id'
    SEND_TO = 'send_to'
    USERS = 'users'
