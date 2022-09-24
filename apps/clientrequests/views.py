from typing import Any, Union
from django.db.models import Q
from django.db.models.query import QuerySet
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.clientrequests.api.serializers.client_request_serializer import (
    ClientRequestCreateSerializer,
)
from apps.clientrequests.models import Client, ClientRequest, RequestType
from apps.hawksbillapi.helpers import GenericResponse
from apps.hawksbillapi.mixins import AuthTokenMixin
from apps.users.models import User


class RequestTypeAPIView(AuthTokenMixin, APIView, GenericResponse):
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        queryset: QuerySet[RequestType] = RequestType.objects.filter(status=True)
        data = [
            {"value": f"{request_type.id}", "detail": request_type.name}
            for request_type in queryset
        ]
        return self.data_response(data=data)


class ClientAPIView(AuthTokenMixin, APIView, GenericResponse):
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        queryset: QuerySet[Client] = Client.objects.filter(status=True)
        data = [{"value": f"{client.id}", "detail": client.name} for client in queryset]
        return self.data_response(data=data)


class TechnicianAPIView(AuthTokenMixin, APIView, GenericResponse):
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        token: Union[Token, None] = Token.objects.filter(
            key=self.get_key(request=request)
        ).first()
        if token is not None:
            user: User = token.user
            queryset: QuerySet[User] = User.objects.filter(is_active=True).filter(
                ~Q(username=user.username)
            )
            data = [
                {
                    "value": f"{technician.id}",
                    "detail": f"{technician.first_name} {technician.last_name}",
                }
                for technician in queryset
            ]
            return self.data_response(data=data)
        return self.missing_http_parameters


class ClientRequestAPIView(AuthTokenMixin, APIView, GenericResponse):
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        request_serializer: ClientRequestCreateSerializer = (
            ClientRequestCreateSerializer(data=request.data)
        )
        if request_serializer.is_valid():
            request_serializer.save()
            return self.redirect_response(redirect_url="/openrequest")
        else:
            return self.data_errors_response(errors=request_serializer.errors)


class CancelClientRequestAPIView(AuthTokenMixin, APIView, GenericResponse):
    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        request_id = request.data.get("id", "0")
        client_request: Union[ClientRequest, None] = ClientRequest.objects.filter(
            id=int(request_id)
        ).first()
        if client_request is not None:
            client_request.delete()
            return self.redirect_response(redirect_url="/openrequest")
        else:
            return self.missing_http_parameters


class CloseClientRequestAPIView(AuthTokenMixin, APIView, GenericResponse):
    def put(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        request_id = request.data.get("id", "0")
        client_request: Union[ClientRequest, None] = ClientRequest.objects.filter(
            id=int(request_id)
        ).first()
        if client_request is not None:
            client_request.is_closed = True
            client_request.save()
            return self.redirect_response(redirect_url="/openrequest")
        else:
            return self.missing_http_parameters
