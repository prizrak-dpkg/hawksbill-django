from typing import Any, Dict, Tuple, Union
from django.db.models.query import QuerySet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.hawksbillapi.helpers import GenericResponse
from apps.hawksbillapi.mixins import AuthTokenMixin
from apps.users.api.serializers.user_serializer import (
    UserListSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
)
from apps.users.models import User


class UserViewSet(AuthTokenMixin, ModelViewSet, GenericResponse):
    def get_serializer(self, *args, **kwargs) -> UserListSerializer:
        serializer_class: UserListSerializer = UserListSerializer
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def get_queryset(
        self, pk: Union[int, None] = None
    ) -> Union[Dict[str, Any], QuerySet[User], None]:
        fields: Tuple[str] = (
            "id",
            "username",
            "document_number",
            "first_name",
            "last_name",
            "email",
            "position",
            "profile_image",
        )
        if pk is not None:
            return (
                self.get_serializer()
                .Meta.model.objects.filter(id=pk, is_active=True)
                .values(*fields)
                .first()
            )
        else:
            return (
                self.get_serializer()
                .Meta.model.objects.filter(is_active=True)
                .values(*fields)
            )

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        user_serializer: UserListSerializer = self.get_serializer(
            instance=self.get_queryset(), many=True
        )
        return self.data_response(data=user_serializer.data)

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        user_serializer: UserCreateSerializer = UserCreateSerializer(
            data=request.data, context=request.data
        )
        if user_serializer.is_valid():
            user_serializer.save()
            return self.message_response(
                "El usuario a sido creado correctamnete.\n"
                + "Compruebe periódicamente su correo electrónico.\n"
                + "En breve, uno de nuestros funcionarios activará su cuenta y se lo notificará."
            )
        else:
            return self.data_errors_response(errors=user_serializer.errors)

    def update(
        self, request: Request, pk: Union[int, None] = None, *args: Any, **kwargs: Any
    ) -> Response:
        user: Union[User, None] = User.objects.filter(id=pk).first()
        if user is not None:
            user_data: Dict[str, str] = {
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "position": user.position,
                "password": user.password,
            }
            user_data.update(request.data)
            user_serializer: UserUpdateSerializer = UserUpdateSerializer(
                instance=user, data=user_data, context=user_data
            )
            if user_serializer.is_valid():
                user_serializer.save()
                return self.data_response(data=self.get_queryset(pk=pk))
            else:
                return self.data_errors_response(errors=user_serializer.errors)
        else:
            return self.message_bad_request("Usuario no encontrado.")

    def destroy(
        self, request: Request, pk: Union[int, None] = None, *args: Any, **kwargs: Any
    ) -> Response:
        user: Union[User, None] = User.objects.filter(id=pk).first()
        if user is not None:
            user.is_active = False
            user.save()
            return self.deleted_instance("Usuario eliminado.")
        else:
            return self.message_bad_request("Usuario no encontrado.")
