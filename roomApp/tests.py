from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from django.test import TestCase
from .consumers import ChatConsumer
from .models import Room


class WebSocketTests(TestCase):
    @database_sync_to_async
    def create_room(self, room_name):
        return Room.objects.create(name=room_name, slug=room_name)

    async def test_connect(self):
        room_name = "test_room"
        room = await self.create_room(room_name)

        path = f"/ws/{room_name}/"
        communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), path)
        connected, _ = await communicator.connect()

        self.assertTrue(connected)

    async def test_disconnect(self):
        room_name = "test_room"
        room = await self.create_room(room_name)

        communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), f"/ws/{room_name}/")
        connected, _ = await communicator.connect()

        self.assertTrue(connected)

        await communicator.disconnect()

