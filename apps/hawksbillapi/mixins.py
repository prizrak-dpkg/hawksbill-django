from datetime import timedelta
from typing import Any, Dict, Tuple, Union
from django.conf import settings
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, get_authorization_header
from apps.hawksbillapi.helpers import GenericResponse

from apps.users.models import User


class AuthTokenMixin(TokenAuthentication, GenericResponse):
    """
    Abstract class mixin that gives access mixins the same customizable
    functionality.
    """

    def get_key(self, request: Request) -> Union[str, None]:
        auth = get_authorization_header(request=request).split()
        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None
        elif len(auth) != 2:
            return None
        else:
            try:
                return auth[1].decode()
            except UnicodeError:
                return None

    def token_expired(self, token: Token) -> bool:
        time_elapsed: timedelta = timezone.now() - token.created
        time_remaining = timedelta(seconds=settings.EXPIRATION_SECONDS) - time_elapsed
        return time_remaining < timedelta()

    def authenticate_credentials(
        self, key
    ) -> Tuple[Union[User, None], Union[Token, None], Dict[str, str]]:
        errors = {}
        token: Union[Token, None] = (
            Token.objects.select_related("user").filter(key=key).first()
        )
        if token is None:
            errors.update({"token": "El token no es válido."})
            return (None, None, errors)
        else:
            if not token.user.is_active:
                errors.update(
                    {
                        "token": "El usuario asociado al token está inactivo"
                        + " o ha sido eliminado."
                    }
                )
                return (None, None, errors)
            else:
                if self.token_expired(token=token):
                    ...
                return (token.user, token, errors)

    def dispatch(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        key: Union[str, None] = self.get_key(request=request)
        if key is not None:
            user: Union[User, None]
            token: Union[Token, None]
            errors: Dict[str, str]
            user, token, errors = self.authenticate_credentials(key=key)
            if user is not None:
                return super().dispatch(request, *args, **kwargs)
            else:
                return self.response_involved(self.data_errors_response(errors=errors))
        else:
            return self.response_involved(
                self.message_bad_request(
                    "No se han proporcionado credenciales."
                    + " Debe autenticarse pasando la clave del token en la cabecera"
                    + ' "Authorization" precedido de la cadena "Token".'
                    + "  Por ejemplo: Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a."
                )
            )
