import contextlib

from apps.directory.models import Map
from apps.tactic.exceptions.tactic import TacticDataError
from apps.tactic.models import UserRoomRelation
from apps.tactic.services.events import Event, Field, SendTo


class TacticService:
    @classmethod
    async def get_response(cls, data, user, room):
        event = data.get(Field.EVENT)
        event_func = getattr(cls, f'event_{event}', None)

        with contextlib.suppress(TacticDataError, TypeError):
            return await event_func(data=data, user=user, room=room)
        return {}

    @classmethod
    async def event_get_map(cls, room, **kwargs):
        return {
            Field.EVENT: Event.GET_MAP,
            Field.SEND_TO: SendTo.ME,
            Field.MAP: room.map_id,
        }

    @classmethod
    async def event_set_map(cls, data, user, room):
        map_id = data.get(Field.MAP)

        if not map_id:
            raise TacticDataError()

        try:
            map = await Map.objects.aget(id=map_id)
        except Map.DoesNotExist:
            raise TacticDataError()

        if not await room.userroomrelation_set.filter(user=user, type=UserRoomRelation.Type.ADMIN).aexists():
            raise TacticDataError()

        room.map = map
        await room.asave()
        return {
            Field.EVENT: Event.SET_MAP,
            Field.SEND_TO: SendTo.EXCEPT_ME,
            Field.MAP: map.id,
        }

    @classmethod
    async def event_get_users(cls, room, **kwargs):
        return {
            Field.EVENT: Event.GET_USERS,
            Field.SEND_TO: SendTo.ALL,
            Field.USERS: [
                {
                    'id': userroomrelation.user_id,
                    'username': userroomrelation.user.username,
                    'type': userroomrelation.type,
                } async for userroomrelation in room.userroomrelation_set.select_related('user').all()
            ],
        }
