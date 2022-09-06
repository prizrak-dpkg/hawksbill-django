from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from apps.clientrequests.models import *


####################
## clientrequests ##
####################


#   =======================   #
#   Table name: RequestType   #
#   =======================   #
class RequestTypeResource(resources.ModelResource):
    class Meta:

        model = RequestType
        import_id_fields = ["id"]


class RequestTypeAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    search_fields = [
        "name",
    ]

    list_display = (
        "id",
        "registration_date",
        "modification_date",
        "status",
        "name",
        "description",
    )

    resource_class = RequestTypeResource


admin.site.register(
    RequestType,
    RequestTypeAdmin,
)


#   =========================   #
#   Table name: ClientRequest   #
#   =========================   #
class ClientRequestResource(resources.ModelResource):
    class Meta:

        model = ClientRequest
        import_id_fields = ["id"]


class ClientRequestAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    search_fields = [
        "name",
    ]

    list_display = (
        "id",
        "registration_date",
        "modification_date",
        "status",
        "type",
        "description",
        "applicant",
        "technician",
        "is_closed",
    )

    resource_class = ClientRequestResource


admin.site.register(
    ClientRequest,
    ClientRequestAdmin,
)
