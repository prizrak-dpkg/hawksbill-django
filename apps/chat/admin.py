from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from apps.chat.models import *


##########
## chat ##
##########


#   ===================   #
#   Table name: Message   #
#   ===================   #
class MessageResource(resources.ModelResource):
    class Meta:

        model = Message
        import_id_fields = ["id"]


class MessageAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    search_fields = [
        "name",
    ]

    list_display = (
        "id",
        "registration_date",
        "modification_date",
        "status",
        "sender",
        "receiver",
        "message",
        "file",
        "url",
    )

    resource_class = MessageResource


admin.site.register(
    Message,
    MessageAdmin,
)
