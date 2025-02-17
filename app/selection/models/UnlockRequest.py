"""
This module defines the UnlockRequest model, which represents a request to unlock a selection.

Classes:
    UnlockRequest: A Django model representing an unlock request for a selection.

Usage:
    This model is used to create and manage unlock requests for selections in the application.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from app.core.models.BaseModel import BaseModel
from app.selection import PENDING
from app.selection import UNLOCK_REQUEST_STATUS_CHOICES
from app.selection.models.Selection import Selection


class UnlockRequest(BaseModel):
    """
    UnlockRequest model represents a request to unlock a selection.

    Attributes:
        selection (OneToOneField): A one-to-one relationship with the Selection model.
        message (TextField): A text field to store the message associated with the unlock request.
        status (CharField): A char field to store the status of the unlock request, with choices
            defined in UNLOCK_REQUEST_STATUS_CHOICES.

    Methods:
        __str__(): Returns a string representation of the UnlockRequest instance.
    """

    selection = models.OneToOneField(Selection, on_delete=models.CASCADE)
    message = models.TextField(verbose_name=_("Message"))
    status = models.CharField(
        max_length=8,
        choices=UNLOCK_REQUEST_STATUS_CHOICES,
        default=PENDING,
        verbose_name=_("Status"),
    )

    def __str__(self):
        """
        Returns a string representation of the UnlockRequest instance.
        The string includes the architect associated with the selection and the status of the unlock request.
        Returns:
            str: A string in the format "UnlockRequest for <architect> - <status>".
        """

        return f"UnlockRequest for {self.selection.architect} - {self.status}"
