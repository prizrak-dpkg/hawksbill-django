from django.urls import path
from apps.clientrequests.channels import (
    OpenRequestWS,
    ClosedRequestWS,
    RequestStatsWS,
    TeamDataWS,
    RequestPercentageWS,
)
from apps.hawksbillapi.views import GetReportAPIView

app_name = "hawksbillapi"

urlpatterns = [
    path("getreport/", GetReportAPIView.as_view(), name="getreport"),
]

websocket_urlpatterns = [
    path("api/openrequest/", OpenRequestWS.as_asgi(), name="openrequest"),
    path("api/closedrequest/", ClosedRequestWS.as_asgi(), name="closedrequest"),
    path("api/teamdata/", TeamDataWS.as_asgi(), name="teamdata"),
    path("api/stats/", RequestStatsWS.as_asgi(), name="stats"),
    path("api/percentage/", RequestPercentageWS.as_asgi(), name="percentage"),
]
