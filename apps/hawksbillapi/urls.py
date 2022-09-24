from django.urls import path
from apps.clientrequests.channels import OpenRequestWS, ClosedRequestWS

app_name = "hawksbillapi"

urlpatterns = []

websocket_urlpatterns = [
    path("api/openrequest/", OpenRequestWS.as_asgi(), name="openrequest"),
    path("api/closedrequest/", ClosedRequestWS.as_asgi(), name="closedrequest"),
]
