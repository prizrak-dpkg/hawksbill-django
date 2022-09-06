from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from apps.hawksbillapi.models import *


##################
## hawksbillapi ##
##################


#   ========================   #
#   Table name: DocumentType   #
#   ========================   #
class DocumentTypeResource(resources.ModelResource):
    class Meta:

        model = DocumentType
        import_id_fields = ["id"]


class DocumentTypeAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    search_fields = [
        "name",
    ]

    list_display = (
        "id",
        "registration_date",
        "modification_date",
        "status",
        "name",
        "acronym",
    )

    resource_class = DocumentTypeResource


admin.site.register(
    DocumentType,
    DocumentTypeAdmin,
)


#   ===================================   #
#   Table name: ConfirmationTokenDetail   #
#   ===================================   #
class ConfirmationTokenDetailResource(resources.ModelResource):
    class Meta:

        model = ConfirmationTokenDetail
        import_id_fields = ["id"]


class ConfirmationTokenDetailAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    search_fields = [
        "detail",
    ]

    list_display = (
        "id",
        "registration_date",
        "modification_date",
        "status",
        "detail",
        "acronym",
    )

    resource_class = ConfirmationTokenDetailResource


admin.site.register(
    ConfirmationTokenDetail,
    ConfirmationTokenDetailAdmin,
)


#   =============================   #
#   Table name: ConfirmationToken   #
#   =============================   #
class ConfirmationTokenResource(resources.ModelResource):
    class Meta:

        model = ConfirmationToken
        import_id_fields = ["token"]


class ConfirmationTokenAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    search_fields = [
        "user__document_number",
    ]

    list_display = (
        "token",
        "user",
        "detail",
    )

    resource_class = ConfirmationTokenResource


admin.site.register(
    ConfirmationToken,
    ConfirmationTokenAdmin,
)
