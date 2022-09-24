import re
from re import Pattern
from typing import Any, Dict, Union, List
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from apps.users.models import User


class GenericResponse:
    """
    Abstract class that provides several types of response.
    """

    @property
    def missing_http_parameters(self) -> Response:
        """
        Method that returns an object of type Response with HTTP status
        code 400 (Bad request) and a message that the request is missing
        HTTP parameters.
        """
        return Response(
            data={
                "response": False,
                "detail": "Missing HTTP parameters",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    @property
    def incorrect_credentials(self) -> Response:
        """
        Method that returns an object of type Response with HTTP status
        code 400 (Bad request) and a message that the information sent
        does not correspond to a registered user.
        """
        return Response(
            data={
                "response": False,
                "message": (
                    "Introduzca un nombre de usuario y contraseña correctos.\n"
                    + "Tenga en cuenta que ambos campos pueden distinguir "
                    + "entre mayúsculas y minúsculas."
                ),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    @property
    def expired_token(self) -> Response:
        """
        Method that returns an object of type Response with HTTP status
        code 401 (Unauthorized) and a message that the request sent
        has an expired token.
        """
        return Response(
            data={
                "response": False,
                "message": "El token ha expirado.",
                "token_is_expired": True,
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    def response_involved(self, response: Response) -> Response:
        """
        Method that returns an object of type Response after setting the properties
        "accepted_renderer", "accepted_media_type" and "renderer_context" for use
        outside a class inherited from "rest_framework".
        """
        response.accepted_renderer: JSONRenderer = JSONRenderer()
        response.accepted_media_type: str = "application/json"
        response.renderer_context: Dict[str, Any] = {}
        return response

    def message_bad_request(self, message: str) -> Response:
        """
        Method that returns an object of type Response with HTTP status
        code 400 (Bad request), which receives a message as a parameter and returns
        it with the response.
        """
        return Response(
            data={
                "response": False,
                "message": message,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def data_errors_response(self, errors: Dict[str, Any]) -> Response:
        """
        Method that returns an object of type Response with HTTP status
        code 400 (Bad request), which receives a dictionary with errors as a
        parameter and returns it with the response.
        """
        return Response(
            data={
                "response": False,
                "errors": errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def data_response(
        self, data: Union[Dict[str, Any], List[Dict[str, Any]]]
    ) -> Response:
        """
        Method that returns an object of type Response with HTTP status
        code 200 (OK), which receives a dictionary with the data as a parameter
        and returns it with the response.
        """
        return Response(
            data={
                "response": True,
                "data": data,
            },
            status=status.HTTP_200_OK,
        )

    def redirect_response(self, redirect_url: str) -> Response:
        """
        Method that returns an object of type Response with HTTP status
        code 200 (OK), which receives a destination URL as a parameter
        and returns it with the response.
        """
        return Response(
            data={
                "response": True,
                "redirect": redirect_url,
            },
            status=status.HTTP_200_OK,
        )

    def message_response(self, message: str) -> Response:
        """
        Method that returns an object of type Response with HTTP status
        code 200 (OK), which receives a message as a parameter and returns
        it with the response.
        """
        return Response(
            data={
                "response": True,
                "message": message,
            },
            status=status.HTTP_200_OK,
        )

    def user_data(self, user: User):
        """
        Method that returns an object of type Response with HTTP status
        code 200 (OK), which receives an object of type User as parameter
        and returns the user information with the response.
        """
        return Response(
            data={
                "response": True,
                "data": {
                    "user": f"{user.first_name} {user.last_name}",
                    "position": user.position,
                    "profile_image": f"{user.profile_image}",
                },
                "username": user.id,
            },
            status=status.HTTP_200_OK,
        )

    def authtoken(self, token: str):
        """
        Method that returns an object of type Response with HTTP status
        code 201 (Created), which receives an authtentication token as a
        parameter and returns it with the response.
        """
        return Response(
            data={
                "response": True,
                "token": token,
            },
            status=status.HTTP_201_CREATED,
        )

    def deleted_instance(self, message: str) -> Response:
        """
        Method that returns an object of type Response with HTTP status
        code 204 (No content), which receives a message as a parameter and returns
        it with the response.
        """
        return Response(
            data={
                "response": True,
                "message": message,
            },
            status=status.HTTP_204_NO_CONTENT,
        )

    class Meta:
        abstract = True


class Helpers:
    """
    Abstract class that provides several types of methods for data manipulation.
    """

    def remove_excess_whitespace(self, string: str) -> str:
        """
        Method that returns a copy of the string with leading and
        trailing whitespace and the excess whitespace between words removed.
        """
        whitespace_regex: Pattern[str] = re.compile(r"(\s)+")
        return re.sub(whitespace_regex, " ", string).strip()

    class Meta:
        abstract = True


class GeneralValidations:
    """
    Abstract class that provides several types of validations.
    """

    def validate_username_pattern(self, username: str) -> bool:
        """
        Method that validates that the string to be evaluated as a
        username has only alphanumeric characters, dots, underscores
        and has at least 4 characters long.
        """
        username_regex: Pattern[str] = re.compile(r"^[a-z._\d]{4,}$", re.IGNORECASE)
        return username_regex.search(username) is not None

    def validate_alphabetic_pattern(self, string: str) -> bool:
        """
        Method that validates that the string entered has only
        alphabetic characters and space characters between words,
        it can also be an empty string.
        """
        alphabetic_regex: Pattern[str] = re.compile(r"^[a-z áéíóú]*$", re.IGNORECASE)
        return alphabetic_regex.search(string) is not None

    def validate_phrase_pattern(self, string: str) -> bool:
        """
        Method that validates that the string entered has only
        alphanumeric characters, space characters between words,
        punctuation marks (. , ; : () [] ' " ¡! ¿?) and basic
        mathematical symbols (+ - / * =).
        It can't be an empty string.
        """
        alphabetic_regex: Pattern[str] = re.compile(
            r"^[\w.áéíóú,;: ()[\]¡!'\"¿?*/+-=]+$", re.IGNORECASE
        )
        return alphabetic_regex.search(string) is not None

    def validate_email_pattern(self, email: str) -> bool:
        """
        Method that validates that the email to be evaluated has an "@"
        character and has a domain following it, complying with the
        structure "user@domain". It must begin with an alphanumeric
        character, then accepts dots, underscores and hyphens.
        """
        email_regex: Pattern[str] = re.compile(
            r"^[a-z\d]{1}[\w.-]{3,}@[\w-]{2,}([.]{1}[\w-]{2,})+$", re.IGNORECASE
        )
        return email_regex.search(email) is not None

    def validate_length_integer_pattern(
        self, integer: Union[str, int], start: int, end: int
    ) -> bool:
        """
        Method that receives as parameter a string or an integer representing
        the integer to be evaluated, a start and an end, and validates that
        the integer has a length between the start and end entered.
        """
        length_of_an_integer: str = "^[\d]{" + f"{start},{end}" + "}$"
        length_of_an_integer_regex: Pattern[str] = re.compile(
            rf"{length_of_an_integer}"
        )
        return length_of_an_integer_regex.search(f"{integer}") is not None

    def validate_password_pattern(self, password: str) -> bool:
        """
        Method that validates that the password is at least 8 characters
        long, uses upper and lower case and uses 1 or more numbers.
        """
        lower_case_regex: Pattern[str] = re.compile(r"[a-z]+")
        upper_case_regex: Pattern[str] = re.compile(r"[A-Z]+")
        digit_regex: Pattern[str] = re.compile(r"\d+")
        greater_than_eight_regex: Pattern[str] = re.compile(r"[\s\S]{8,}")
        return (
            lower_case_regex.search(password) is not None
            and upper_case_regex.search(password) is not None
            and digit_regex.search(password) is not None
            and greater_than_eight_regex.match(password) is not None
        )

    class Meta:
        abstract = True
