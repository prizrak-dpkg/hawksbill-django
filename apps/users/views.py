import json
from typing import Any, Dict, Union
from django.contrib.sessions.models import Session
from django.db.models.query import QuerySet
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.hawksbillapi.helpers import GenericResponse
from apps.hawksbillapi.mixins import AuthTokenMixin
from apps.hawksbillapi.models import ConfirmationToken
from apps.users.models import User


class HawksbillSessionManagement(GenericResponse):
    """
    Abstract class that provides the login and logout classes with
    the same functionality.
    """

    def clear_active_sessions(self, user: User, token: Token) -> None:
        """
        Method that removes the token from database and clear
        all active user sessions.
        """
        token.delete()
        active_sessions: QuerySet[Session] = Session.objects.filter(
            expire_date__gte=timezone.now()
        )
        for session in active_sessions:
            session_data = session.get_decoded()
            if user.id == int(session_data.get("_auth_user_id")):
                session.delete()

    class Meta:
        abstract = True


class LoginAPIView(ObtainAuthToken, HawksbillSessionManagement):
    """
    Class that has the logic to authenticate a user.
    """

    def get_document_number_by_username_or_email(self, data: str) -> Union[str, None]:
        """
        Method that tries to obtain an object of type User through a
        username or e-mail and returns its document number if it is
        obtained, otherwise it returns a None object.
        """
        if not data.isdigit():
            user: Union[User, None] = User.objects.filter(username=data).first()
            if user is None:
                user: Union[User, None] = User.objects.filter(email=data).first()
            return None if user is None else f"{user.document_number}"
        else:
            return data

    def login(self, data: Dict[str, Union[str, int, None]]) -> Response:
        """
        Method that returns an object of type Response. It uses
        the serializer provided by the ObtainAuthToken class and
        validates the request data (username, password) if valid
        it creates a Token associated to the user and returns it
        in the response.
        """
        login_serializer = self.serializer_class(data=data, context={"request": data})
        if login_serializer.is_valid():
            user: User = login_serializer.validated_data["user"]
            token: Token
            token, created = Token.objects.get_or_create(user=user)
            if not created:
                self.clear_active_sessions(user=user, token=token)
                token = Token.objects.create(user=user)
            return self.authtoken(token=token.key)
        else:
            return self.incorrect_credentials

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        if request.data.get("login") is not None:
            data: Dict[str, Union[str, int, None]] = json.loads(request.data["login"])
            if isinstance(data["username"], str):
                data["username"] = self.get_document_number_by_username_or_email(
                    data["username"]
                )
            return self.login(data=data)
        else:
            return self.missing_http_parameters


class LogoutAPIView(APIView, HawksbillSessionManagement):
    """
    Class that has the logic to logout a user.
    """

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        if request.data.get("token") is not None:
            token: Union[Token, None] = Token.objects.filter(
                key=request.data.get("token")
            ).first()
            if token is not None:
                user: User = token.user
                self.clear_active_sessions(user=user, token=token)
            return self.redirect_response(redirect_url="/login")
        else:
            return self.missing_http_parameters


class ActiveAPIView(APIView, GenericResponse):
    """
    Class that has the logic to activate a user.
    """

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        if request.data.get("token") is not None:
            token: Union[ConfirmationToken, None] = ConfirmationToken.objects.filter(
                token=request.data.get("token")
            ).first()
            if token is not None:
                user: User = token.user
                user.is_active = True
                user.save()
                token.delete()
                return self.message_response(
                    message="Felicidades!\nTu cuenta ya se encuentra activa."
                )
            else:
                return self.message_bad_request(message="El enlace ha caducado.")
        else:
            return self.missing_http_parameters


class UserToken(APIView, GenericResponse):
    """
    Class that has the logic to return a user's token.
    """

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        if request.data.get("username") is not None:
            user: Union[User, None] = User.objects.filter(
                id=request.data["username"]
            ).first()
            if user is not None:
                token: Union[Token, None] = Token.objects.filter(user=user).first()
                if token is not None:
                    return self.authtoken(token=token.key)
        return self.missing_http_parameters


class TokenExpired(AuthTokenMixin, APIView, GenericResponse):
    """
    Class that has the logic to return if user's token is expired.
    """

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return self.message_response("")


class UserData(AuthTokenMixin, APIView, GenericResponse):
    """
    Class that has the logic to return a user's data.
    """

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        token: Union[Token, None] = Token.objects.filter(
            key=self.get_key(request=request)
        ).first()
        if token is not None:
            return self.user_data(user=token.user)
        return self.missing_http_parameters
