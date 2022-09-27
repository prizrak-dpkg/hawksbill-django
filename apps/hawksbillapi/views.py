from typing import Any, Union
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http.response import HttpResponseRedirect
from apps.hawksbillapi.helpers import GenericResponse
from apps.hawksbillapi.mixins import AuthTokenMixin
from apps.hawksbillapi.reports import HawksbillReport


def home_redirect(request: Request, *args: Any, **kwargs: Any) -> HttpResponseRedirect:
    return HttpResponseRedirect("/swagger/")


class GetReportAPIView(AuthTokenMixin, APIView, GenericResponse):
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        token: Union[Token, None] = Token.objects.filter(
            key=self.get_key(request=request)
        ).first()
        start_date: Union[str, None] = request.data.get("startdate")
        end_date: Union[str, None] = request.data.get("enddate")
        if token is not None and start_date is not None and end_date is not None:
            return self.redirect_response(
                redirect_url=HawksbillReport(
                    user=token.user, start_date=start_date, end_date=end_date
                ).get_report
            )
        return self.missing_http_parameters
