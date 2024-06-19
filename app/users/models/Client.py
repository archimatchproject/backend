from django.db import models

from app.users.models.ArchimatchUser import ArchimatchUser
from app.utils.models import BaseModel


class Client(BaseModel):
    """
    Model representing a client in the Archimatch application.

    Attributes:
        user (OneToOneField): Associated ArchimatchUser instance for this client.
    """

    user = models.OneToOneField(ArchimatchUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email

    class Meta:
        """Meta class for Client model."""

        verbose_name = "Client"
        verbose_name_plural = "Clients"
