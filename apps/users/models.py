from django.contrib.auth.models import AbstractUser
from django.db import models


###########
## Users ##
###########


#   ================   #
#   Table name: User   #
#   ================   #
class User(AbstractUser):
    document_number = models.PositiveBigIntegerField(
        verbose_name="Document number",
        unique=True,
        help_text="Required. Digits only.",
        error_messages={
            "unique": "A user with that document number already exists.",
        },
    )
    email = models.EmailField(
        verbose_name="E-mail address",
        unique=True,
        help_text="Format: username@domain.",
        error_messages={
            "unique": "A user with that email already exists.",
        },
    )
    position = models.CharField(
        verbose_name="Position",
        max_length=50,
        blank=True,
        help_text="Position held in the organization, 50 characters or fewer. Letters, digits and @/./+/-/_ only.",
    )
    profile_image = models.ImageField(
        verbose_name="Profile image",
        upload_to="profile/",
        default="assets/images/hawksbill.png",
    )
    USERNAME_FIELD = "document_number"
    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
        "email",
        "position",
    ]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = [
            "email",
        ]

    def __str__(self):
        return "{}".format(
            self.username,
        )
