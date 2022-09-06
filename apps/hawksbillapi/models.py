from django.db import models
from apps.users.models import User


##################
## hawksbillapi ##
##################


#   =====================   #
#   Table name: BaseModel   #
#   =====================   #
class BaseModel(models.Model):
    id = models.AutoField(
        verbose_name="Primary key (A.I)",
        primary_key=True,
    )
    registration_date = models.DateTimeField(
        verbose_name="Registration date",
        auto_now=False,
        auto_now_add=True,
    )
    modification_date = models.DateTimeField(
        verbose_name="Modification date",
        auto_now=True,
        auto_now_add=False,
    )
    status = models.BooleanField(
        verbose_name="Status for logical elimination",
        default=True,
    )

    class Meta:
        abstract = True


#   ========================   #
#   Table name: DocumentType   #
#   ========================   #
class DocumentType(BaseModel):
    name = models.CharField(
        verbose_name="Name",
        max_length=50,
        unique=True,
    )
    acronym = models.CharField(
        verbose_name="Acronym",
        max_length=3,
        unique=True,
    )

    class Meta:
        verbose_name = "Document type"
        verbose_name_plural = "Document types"
        ordering = [
            "name",
        ]

    def __str__(self):
        return "{}".format(
            self.name,
        )


#   ===================================   #
#   Table name: ConfirmationTokenDetail   #
#   ===================================   #
class ConfirmationTokenDetail(BaseModel):
    detail = models.CharField(
        verbose_name="Detail",
        max_length=50,
        unique=True,
    )
    acronym = models.CharField(
        verbose_name="Acronym",
        max_length=3,
        unique=True,
    )

    class Meta:
        verbose_name = "Confirmation token detail"
        verbose_name_plural = "Confirmation token details"
        ordering = [
            "detail",
        ]

    def __str__(self):
        return "{}".format(
            self.detail,
        )


#   =============================   #
#   Table name: ConfirmationToken   #
#   =============================   #
class ConfirmationToken(models.Model):
    token = models.CharField(
        verbose_name="Token",
        max_length=40,
        primary_key=True,
    )
    user = models.ForeignKey(
        verbose_name="User",
        to=User,
        on_delete=models.PROTECT,
    )
    detail = models.ForeignKey(
        verbose_name="Detail",
        to=ConfirmationTokenDetail,
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = "Confirmation token"
        verbose_name_plural = "Confirmation tokens"
        ordering = [
            "user",
            "detail",
        ]

    def __str__(self):
        return "{}".format(
            self.token,
        )
