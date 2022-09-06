from django.db import models
from apps.hawksbillapi.models import BaseModel
from apps.users.models import User


##########
## chat ##
##########


#   ===================   #
#   Table name: Message   #
#   ===================   #
class Message(BaseModel):
    sender = models.ForeignKey(
        verbose_name="Sender",
        to=User,
        on_delete=models.PROTECT,
        related_name="user_delivers",
    )
    receiver = models.ForeignKey(
        verbose_name="Receiver",
        to=User,
        on_delete=models.PROTECT,
        related_name="user_receives",
    )
    message = models.TextField(
        verbose_name="Message",
        blank=True,
        null=True,
    )
    file = models.FileField(
        verbose_name="File",
        blank=True,
        null=True,
    )
    url = models.URLField(
        verbose_name="URL",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = [
            "-modification_date",
        ]

    def __str__(self):
        return "{}".format(
            self.sender,
        )
