import json
from asgiref.sync import sync_to_async
from datetime import timedelta
from typing import Any, Dict, List, Union
from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from channels.generic.websocket import AsyncWebsocketConsumer
from apps.clientrequests.models import ClientRequest
from apps.hawksbillapi.helpers import GenericResponse
from apps.users.models import User


class GetRequestData:
    def get_data(
        self, key: str, is_closed: bool = False
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        token: Union[Token, None] = Token.objects.filter(key=key).first()
        if token is not None:
            user: User = token.user
            queryset: QuerySet[ClientRequest] = ClientRequest.objects.filter(
                status=True, is_closed=is_closed
            )
            data = [
                {
                    "id": open_request.id,
                    "registration_date": (
                        open_request.registration_date - timedelta(hours=5)
                    ).strftime("%b %d %Y %H:%M:%S"),
                    "modification_date": (
                        open_request.modification_date - timedelta(hours=5)
                    ).strftime("%b %d %Y %H:%M:%S"),
                    "client": open_request.client.name,
                    "client_image": f"{open_request.client.logo}",
                    "request_type": open_request.type.name,
                    "description": open_request.description,
                    "applicant": {
                        "detail": f"{open_request.applicant.first_name} {open_request.applicant.last_name}",
                        "check": open_request.applicant == user,
                    },
                    "technician": {
                        "detail": f"{open_request.technician.first_name} {open_request.technician.last_name}",
                        "check": open_request.technician == user,
                    },
                    "is_closed": open_request.is_closed,
                }
                for open_request in queryset
            ]
            return data
        return {
            "data": {
                "response": False,
                "detail": "Missing HTTP parameters",
            },
            "status": status.HTTP_400_BAD_REQUEST,
        }

    async def disconnect(self, code) -> None:
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def server_response(self, data):
        server_message = {
            "data": data["data"],
            "status": status.HTTP_200_OK,
        }
        await self.send(json.dumps(server_message))


class OpenRequestWS(AsyncWebsocketConsumer, GetRequestData):
    async def connect(self) -> None:
        self.room_group_name: str = "open_requests"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        key: str = json.loads(text_data)["key"]
        data: Dict[str, Any] = await sync_to_async(
            self.get_data,
        )(key=key)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "server_response",
                "data": data,
            },
        )


class ClosedRequestWS(AsyncWebsocketConsumer, GetRequestData):
    async def connect(self) -> None:
        self.room_group_name: str = "closed_requests"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        key: str = json.loads(text_data)["key"]
        data: Dict[str, Any] = await sync_to_async(
            self.get_data,
        )(key=key, is_closed=True)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "server_response",
                "data": data,
            },
        )
