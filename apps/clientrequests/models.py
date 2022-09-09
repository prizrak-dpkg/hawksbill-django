from django.db import models
from ckeditor.fields import RichTextField
from apps.hawksbillapi.models import BaseModel
from apps.users.models import User


####################
## clientrequests ##
####################


#   ==================   #
#   Table name: Client   #
#   ==================   #
class Client(BaseModel):
    name = models.CharField(
        verbose_name="Name",
        max_length=50,
        unique=True,
    )
    logo = models.ImageField(
        verbose_name="Logo",
        upload_to="client/",
        default="assets/images/hawksbill.png",
    )

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = [
            "name",
        ]

    def __str__(self):
        return "{}".format(
            self.name,
        )


#   =======================   #
#   Table name: RequestType   #
#   =======================   #
class RequestType(BaseModel):
    name = models.CharField(
        verbose_name="Name",
        max_length=50,
        unique=True,
    )
    description = RichTextField(
        verbose_name="Description",
    )

    class Meta:
        verbose_name = "Request type"
        verbose_name_plural = "Request types"
        ordering = [
            "name",
        ]

    def __str__(self):
        return "{}".format(
            self.name,
        )


#   =========================   #
#   Table name: ClientRequest   #
#   =========================   #
class ClientRequest(BaseModel):
    client = models.ForeignKey(
        verbose_name="Client",
        to=Client,
        on_delete=models.PROTECT,
    )
    type = models.ForeignKey(
        verbose_name="Request type",
        to=RequestType,
        on_delete=models.PROTECT,
    )
    description = models.TextField(
        verbose_name="Description",
    )
    applicant = models.ForeignKey(
        verbose_name="¿Who delivers?",
        to=User,
        on_delete=models.PROTECT,
        related_name="applicant",
    )
    technician = models.ForeignKey(
        verbose_name="¿Who receives?",
        to=User,
        on_delete=models.PROTECT,
        related_name="technician",
    )
    is_closed = models.BooleanField(
        verbose_name="¿Has the request been closed?",
        default=False,
    )

    class Meta:
        verbose_name = "Request"
        verbose_name_plural = "Requests"
        ordering = [
            "applicant",
        ]

    def __str__(self):
        return "{}".format(
            self.applicant,
        )
