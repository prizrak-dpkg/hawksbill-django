from django.urls import path
from apps.clientrequests.views import (
    RequestTypeAPIView,
    ClientAPIView,
    TechnicianAPIView,
    ClientRequestAPIView,
    CancelClientRequestAPIView,
    CloseClientRequestAPIView,
)


app_name = "clientrequests"

urlpatterns = [
    path("requesttype/", RequestTypeAPIView.as_view(), name="requesttype"),
    path("clients/", ClientAPIView.as_view(), name="clients"),
    path("technicians/", TechnicianAPIView.as_view(), name="technicians"),
    path("clientrequest/", ClientRequestAPIView.as_view(), name="clientrequest"),
    path(
        "cancelopenrequest/",
        CancelClientRequestAPIView.as_view(),
        name="cancelopenrequest",
    ),
    path(
        "closeopenrequest/",
        CloseClientRequestAPIView.as_view(),
        name="closeopenrequest",
    ),
]
