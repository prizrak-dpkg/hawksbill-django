from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from apps.documents.models import *


###############
## documents ##
###############


#   ====================   #
#   Table name: Software   #
#   ====================   #
class SoftwareResource(resources.ModelResource):
    class Meta:

        model = Software
        import_id_fields = ["id"]


class SoftwareAdmin(ImportExportModelAdmin, admin.ModelAdmin):

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

    resource_class = SoftwareResource


admin.site.register(
    Software,
    SoftwareAdmin,
)


#   ===========================   #
#   Table name: LicensingTables   #
#   ===========================   #
class LicensingTablesResource(resources.ModelResource):
    class Meta:

        model = LicensingTables
        import_id_fields = ["id"]


class LicensingTablesAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    search_fields = [
        "serial_number",
        "software__name",
    ]

    list_display = (
        "id",
        "registration_date",
        "modification_date",
        "status",
        "software",
        "serial_number",
        "activation_date",
        "days",
        "description",
        "is_active",
    )

    resource_class = LicensingTablesResource


admin.site.register(
    LicensingTables,
    LicensingTablesAdmin,
)


#   =======================   #
#   Table name: Credentials   #
#   =======================   #
class CredentialsResource(resources.ModelResource):
    class Meta:

        model = Credentials
        import_id_fields = ["id"]


class CredentialsAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    search_fields = [
        "platform",
        "access_url",
        "user",
    ]

    list_display = (
        "id",
        "registration_date",
        "modification_date",
        "status",
        "platform",
        "access_url",
        "user",
        "password",
        "comments",
    )

    resource_class = CredentialsResource


admin.site.register(
    Credentials,
    CredentialsAdmin,
)
