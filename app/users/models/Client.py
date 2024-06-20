"""
Module: Client Model

This module defines the Client model, representing a client in the Archimatch application.

Classes:
    Client: Model representing a client.

"""

from django.db import models

from app.users.models import ArchimatchUser
from app.utils.models import BaseModel


class Client(BaseModel):
    """
    Model representing a client in the Archimatch application.

    Attributes:
        user (OneToOneField): Associated ArchimatchUser instance for this client.
    """

    user = models.OneToOneField(ArchimatchUser, on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns the email address of the associated user.

        Returns:
            str: Email address of the client's associated user.
        """
        return self.user.email

    class Meta:
        """
        Meta class for Client model.

        Attributes:
            verbose_name (str): Singular name for the model used in the Django admin interface.
            verbose_name_plural (str): Plural name for the model used in the Django admin interface.
        """

        verbose_name = "Client"
        verbose_name_plural = "Clients"
