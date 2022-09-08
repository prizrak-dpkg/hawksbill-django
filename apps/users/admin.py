from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserBaseAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from apps.users.models import *


###########
## Users ##
###########


#   ================   #
#   Table name: User   #
#   ================   #
class UserResource(resources.ModelResource):
    class Meta:
        model = User


class UserAdmin(UserBaseAdmin, ImportExportModelAdmin, admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("document_number", "username", "password")}),
        (
            ("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "position",
                    "profile_image",
                )
            },
        ),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "document_number", "password1", "password2"),
            },
        ),
    )
    search_fields = [
        "username",
        "document_number",
        "email",
    ]
    list_display = (
        "id",
        "date_joined",
        "last_login",
        "is_superuser",
        "is_staff",
        "is_active",
        "username",
        "document_number",
        "first_name",
        "last_name",
        "email",
        "position",
        "profile_image",
    )
    resource_class = UserResource


admin.site.register(
    User,
    UserAdmin,
)
