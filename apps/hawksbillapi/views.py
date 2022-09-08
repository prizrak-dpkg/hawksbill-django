from typing import Any
from rest_framework.request import Request
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy


def home_redirect(request: Request, *args: Any, **kwargs: Any) -> HttpResponseRedirect:
    return HttpResponseRedirect("/swagger/")
