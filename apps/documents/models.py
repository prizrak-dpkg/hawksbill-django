from django.db import models
from apps.hawksbillapi.models import BaseModel


###############
## documents ##
###############


#   ====================   #
#   Table name: Software   #
#   ====================   #
class Software(BaseModel):
    name = models.CharField(
        verbose_name="Name",
        max_length=50,
        unique=True,
    )
    description = models.TextField(
        verbose_name="Description",
    )

    class Meta:
        verbose_name = "Software"
        verbose_name_plural = "Software"
        ordering = [
            "name",
        ]

    def __str__(self):
        return "{}".format(
            self.name,
        )


#   ===========================   #
#   Table name: LicensingTables   #
#   ===========================   #
class LicensingTables(BaseModel):
    software = models.ForeignKey(
        verbose_name="Software",
        to=Software,
        on_delete=models.PROTECT,
    )
    serial_number = models.CharField(
        verbose_name="Serial number",
        max_length=50,
        unique=True,
    )
    activation_date = models.DateField(
        verbose_name="Activation date",
        blank=True,
        null=True,
    )
    days = models.PositiveIntegerField(
        verbose_name="Number of days",
    )
    description = models.TextField(
        verbose_name="Description",
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(
        verbose_name="¿Is the license active?",
        default=True,
    )

    class Meta:
        verbose_name = "Licensing table"
        verbose_name_plural = "Licensing tables"
        ordering = [
            "-modification_date",
        ]

    def __str__(self):
        return "{}".format(
            self.serial_number,
        )


#   =======================   #
#   Table name: Credentials   #
#   =======================   #
class Credentials(BaseModel):
    platform = models.CharField(
        verbose_name="Platform",
        max_length=50,
    )
    access_url = models.URLField(
        verbose_name="Access URL",
    )
    user = models.CharField(
        verbose_name="User",
        max_length=50,
    )
    password = models.CharField(
        verbose_name="Password",
        max_length=128,
    )
    comments = models.TextField(
        verbose_name="Comments",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Credential"
        verbose_name_plural = "Credentials"
        ordering = [
            "platform",
        ]

    def __str__(self):
        return "{}".format(
            self.platform,
        )
