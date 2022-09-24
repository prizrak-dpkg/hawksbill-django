from typing import Any, Dict, Union
from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
)
from apps.clientrequests.models import Client, ClientRequest, RequestType
from apps.hawksbillapi.helpers import GeneralValidations, Helpers
from apps.users.models import User


class ClientRequestCreateSerializer(ModelSerializer, GeneralValidations, Helpers):
    class Meta:
        model = ClientRequest
        fields = (
            "client",
            "type",
            "description",
            "applicant",
            "technician",
        )

    def validate_client(self, data: Union[Client, Any]) -> Client:
        if not isinstance(data, Client):
            raise ValidationError(
                "El cliente que intenta asignar no es válido."
                + "\nAsegúrese de que el los datos ingresados sean"
                + " correctos e intente de nuevo."
            )
        else:
            return data

    def validate_type(self, data: Union[RequestType, Any]) -> RequestType:
        if not isinstance(data, RequestType):
            raise ValidationError(
                "El tipo de solicitud intenta asignar no es válido."
                + "\nAsegúrese de que el los datos ingresados sean"
                + " correctos e intente de nuevo."
            )
        else:
            return data

    def validate_applicant(self, data: Union[User, Any]) -> User:
        if not isinstance(data, User):
            raise ValidationError(
                "El usuario que realiza la petición no es válido."
                + "\nAsegúrese de que el los datos ingresados sean"
                + " correctos e intente de nuevo."
            )
        else:
            return data

    def validate_description(self, data: str) -> User:
        if not self.validate_phrase_pattern(string=data):
            raise ValidationError(
                "La descripción de la tarea no es válida."
                + "\nAsegúrese de que la descripción ingresada solo"
                + " tenga caracteres alfanuméricos, caracteres de"
                + " espacio entre palabras, signos de puntuación"
                + " (, ; : () [] ' \" ¡! ¿?) y los símbolos símbolos"
                + " matemáticos básicos (+ - / * =)."
                + " No puede ser una cadena vacía."
            )
        else:
            return self.remove_excess_whitespace(data)

    def validate_technician(self, data: Union[User, Any]) -> User:
        if not isinstance(data, User):
            raise ValidationError(
                "El usuario que realiza la petición no es válido."
                + "\nAsegúrese de que el los datos ingresados sean"
                + " correctos e intente de nuevo."
            )
        else:
            return data

    def create(self, validated_data: Dict[str, Any]) -> User:
        client_request = ClientRequest(**validated_data)
        client_request.save()
        return client_request
