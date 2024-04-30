import contextlib

from django.db import IntegrityError

from apps.core.models import User
from apps.tactic.models import Room
from apps.tactic.services.events import SendTo
from apps.tactic.services.tactic import TacticService
from generic.authentications.channels import AuthAsyncJsonWebsocketConsumer


class TacticConsumer(AuthAsyncJsonWebsocketConsumer):
    async def connect(self):
        await super().connect()

        room_uuid = self.scope['url_route']['kwargs'].get('room_uuid')

        try:
            self.room = await Room.objects.aget(uuid=room_uuid)
        except Room.DoesNotExist:
            await self.close()

        await self.accept()
        await self.channel_layer.group_add(self.get_room_name(self.user), self.channel_name)
        with contextlib.suppress(IntegrityError):
            await self.room.userroomrelation_set.acreate(user=self.user)

    async def disconnect(self, code):
        await self.room.users.aremove(self.user)
        await self.channel_layer.group_discard(self.get_room_name(self.user), self.channel_name)

    async def receive_json(self, content, **kwargs):
        response = await TacticService.get_response(data=content, user=self.user, room=self.room)
        await self.send_response(response)

    async def tactic_message(self, event):
        await self.send_json(content=event)

    async def send_response(self, response: dict | list):
        if isinstance(response, list):
            for resp in response:
                await self.send_response_object(resp)
        else:
            await self.send_response_object(response)

    async def send_response_object(self, response: dict):
        send_to = response.get('send_to')
        response['type'] = 'tactic.message'
        match send_to:
            case SendTo.ALL:
                async for user in self.room.users.all():
                    await self.channel_layer.group_send(self.get_room_name(user), response)
            case SendTo.EXCEPT_ME:
                async for user in self.room.users.exclude(id=self.user.id):
                    await self.channel_layer.group_send(self.get_room_name(user), response)
            case SendTo.ME:
                await self.channel_layer.group_send(self.get_room_name(self.user), response)

    def get_room_name(self, user: User):
        return f'{self.room.uuid.hex}-{user.username}'
