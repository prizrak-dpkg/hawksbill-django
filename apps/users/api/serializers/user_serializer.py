from collections import OrderedDict
from typing import Any, Dict, Union
from django.core import exceptions
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework.serializers import (
    CharField,
    EmailField,
    IntegerField,
    ModelSerializer,
    ValidationError,
)
from rest_framework.validators import UniqueValidator
from apps.hawksbillapi.helpers import GeneralValidations, Helpers
from apps.hawksbillapi.models import ConfirmationToken, ConfirmationTokenDetail
from apps.users.models import User


class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "document_number",
            "first_name",
            "last_name",
            "email",
            "position",
            "profile_image",
        )

    def to_representation(self, instance: Dict[str, Any]):
        return OrderedDict(
            {
                "id": instance.get("id"),
                "username": instance.get("username"),
                "document_number": instance.get("document_number"),
                "first_name": instance.get("first_name"),
                "last_name": instance.get("last_name"),
                "email": instance.get("email"),
                "position": instance.get("position"),
                "profile_image": f'{instance.get("profile_image")}',
            }
        )


class UserCreateSerializer(ModelSerializer, GeneralValidations):
    class Meta:
        model = User
        fields = (
            "document_number",
            "email",
            "password",
        )

    document_number: IntegerField = IntegerField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all().values("document_number"),
                message="El número de documento ya se encuentra registrado."
                + "\nIntente recuperar su cuenta.",
            )
        ]
    )
    email: EmailField = EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all().values("email"),
                message="El e-mail ya se encuentra registrado."
                + "\nIntente recuperar su cuenta.",
            )
        ]
    )

    def validate_document_number(self, data: Union[str, int]) -> int:
        if not self.validate_length_integer_pattern(integer=data, start=4, end=10):
            raise ValidationError(
                "El número de documento no es válido."
                + "\nAsegúrese de que el número ingresado tiene entre 4 y 10 dígitos."
            )
        else:
            return int(data)

    def validate_email(self, data: str) -> str:
        if not self.validate_email_pattern(data):
            raise ValidationError(
                "El e-mail no es válido."
                + "\nAsegúrese de que el e-mail:"
                + '\n* Cumpla con la estructura "user@doma.in".'
                + "\n* Empieza con un carácter alfanumérico [a-z0-9]."
            )
        else:
            return data.lower()

    def validate_password(self, data: str) -> str:
        if not self.validate_password_pattern(password=data):
            raise ValidationError(
                "La contraseña ingresada es demasiado débil."
                + "\nAsegúrese de que la contraseña tiene al menos:"
                + "\n* 8 caracteres."
                + "\n* Utiliza letras mayúsculas y minúsculas."
                + "\n* Emplea uno o más números."
            )
        elif f'{self.context.get("document_number")}' in data:
            raise ValidationError(
                "La contraseña no puede contener el número de documento."
            )
        else:
            return make_password(data)

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        attrs["username"] = f'{attrs.get("document_number")}'
        attrs["is_active"] = False
        return super().validate(attrs)

    def create(self, validated_data: Dict[str, Any]) -> User:
        confirmation_token_detail = ConfirmationTokenDetail.objects.filter(
            acronym="NU"
        ).first()
        if confirmation_token_detail is None:
            raise exceptions.ImproperlyConfigured(
                f"{self.__class__.__name__} is missing the 'NU'"
                + " confirmation token detail record. Define the 'NU'"
                + " confirmation token detail record in the"
                + " ConfirmationTokenDetail table."
            )
        else:
            user = User(**validated_data)
            user.save()
            ConfirmationToken(
                token=Token.generate_key(), user=user, detail=confirmation_token_detail
            ).save()
            return user


class UserUpdateSerializer(UserCreateSerializer, GeneralValidations, Helpers):
    instance: User

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "position",
            "profile_image",
            "password",
        )

    username: CharField = CharField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all().values("username"),
                message="El nombre de usuario ya se encuentra en uso.\n"
                + "Intente con otro.",
            )
        ]
    )

    email: EmailField = EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all().values("email"),
                message="El e-mail ya se encuentra en uso.\n" + "Intente con otro.",
            )
        ]
    )

    def validate_username(self, data: str) -> str:
        if not self.validate_username_pattern(data):
            raise ValidationError(
                "El nombre de usuario no es válido."
                + "\nAsegúrese de que el nombre de usuario:"
                + "\n* No tenga espacios o caracteres especiales."
                + "\n* Este formado por caracteres alfanuméricos [a-z0-9]."
                + "\n* Adicionalmente, sólo se permiten puntos o guiones bajos [_.]."
            )
        else:
            return data.lower()

    def validate_first_name(self, data: str) -> str:
        if not self.validate_alphabetic_pattern(data):
            raise ValidationError(
                "Los nombres ingresados no son válidos."
                + "\nAsegúrese de que los nombres:"
                + "\n* No tengan caracteres especiales."
                + "\n* Esten formados por caracteres alfabéticos [a-z áéíóú]."
            )
        else:
            return self.remove_excess_whitespace(data).capitalize()

    def validate_last_name(self, data: str) -> str:
        if not self.validate_alphabetic_pattern(data):
            raise ValidationError(
                "Los apellidos ingresados no son válidos."
                + "\nAsegúrese de que los apellidos:"
                + "\n* No tengan caracteres especiales."
                + "\n* Esten formados por caracteres alfabéticos [a-z áéíóú]."
            )
        else:
            return self.remove_excess_whitespace(data).capitalize()

    def validate_email(self, data: str) -> str:
        if not self.instance.email == data:
            return super().validate_email(data)
        else:
            return data

    def validate_position(self, data: str) -> str:
        if not self.validate_alphabetic_pattern(data):
            raise ValidationError(
                "El cargo ingresado no es válido."
                + "\nAsegúrese de que el cargo:"
                + "\n* No tengan caracteres especiales."
                + "\n* Este formado por caracteres alfabéticos [a-z áéíóú]."
            )
        else:
            return self.remove_excess_whitespace(data).capitalize()

    def validate_password(self, data: str) -> str:
        current_raw_password = self.context.get("current_raw_password")
        if current_raw_password is not None:
            if not self.instance.check_password(current_raw_password):
                raise ValidationError("La contraseña actual es incorrecta.")
            else:
                return super().validate_password(data)
        else:
            if not self.instance.password == data:
                raise ValidationError(
                    'La contraseña actual debe enviarse como "current_raw_password"'
                    + " junto con la nueva contraseña para realizar el cambio."
                )
            else:
                return data

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        if not self.instance.email == attrs.get("email"):
            attrs["is_active"] = False
        return attrs

    def update(self, instance: User, validated_data: Dict[str, Any]):
        confirmation_token_detail = ConfirmationTokenDetail.objects.filter(
            acronym="UU"
        ).first()
        if confirmation_token_detail is None:
            raise exceptions.ImproperlyConfigured(
                f"{self.__class__.__name__} is missing the 'UU'"
                + " confirmation token detail record. Define the 'UU'"
                + " confirmation token detail record in the"
                + " ConfirmationTokenDetail table."
            )
        else:
            user = super().update(instance, validated_data)
            user.save()
            if not user.is_active:
                ConfirmationToken(
                    token=Token.generate_key(),
                    user=user,
                    detail=confirmation_token_detail,
                ).save()
            return user
