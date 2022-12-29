import json
from typing import Any

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Message, Room


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None

    def connect(self) -> None:
        """
        Configure and accept incoming Web Socket requests from client.
        """
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.room = Room.objects.get(name=self.room_name)  # Synchronous DB call
        self.user = self.scope["user"]

        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.send(
            json.dumps(
                {
                    #  TODO: Add ENUM for chat event types.
                    "type": "user.list",
                    "users": [user.username for user in self.room.online.all()],
                }
            )
        )

        if self.user.is_authenticated:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "user.join",
                    "user": self.user.username,
                },
            )
            self.room.online.add(self.user)

    def disconnect(self, close_code: str) -> None:
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

        if self.user.is_authenticated:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "user.leave",
                    "user": self.user.username,
                },
            )
            self.room.online.remove(self.user)

    def receive(
        self, text_data: str | None = None, bytes_data: bytes | None = None
    ) -> None:
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        if not self.user.is_authenticated:
            return

        # send chat message event to the room
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat.message",
                "user": self.user.username,
                "message": message,
            },
        )

    def chat_message(self, event: dict[str, Any]) -> None:
        self.send(text_data=json.dumps(event))

    def user_join(self, event: dict[str, Any]) -> None:
        self.send(text_data=json.dumps(event))

    def user_leave(self, event: dict[str, Any]) -> None:
        self.send(text_data=json.dumps(event))
