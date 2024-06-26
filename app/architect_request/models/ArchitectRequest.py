"""
Module containing the ArchitectRequest model.

This module defines the ArchitectRequest model, which includes additional fields and relationships
specific to architects within the Archimatch application.

Classes:
    ArchitectRequest: Defines the ArchitectRequest model with additional fields and relationships.
"""

from django.db import models

from app.architect_request.models.Meeting import Meeting
from app.core.models import BaseModel
from app.core.models.ArchitectSpeciality import ArchitectSpeciality


class ArchitectRequest(BaseModel):
    """
    Defines the ArchitectRequest model with additional fields and relationships.

    Fields:
        first_name (CharField): The first name of the architect.
        last_name (CharField): The last name of the architect.
        phone_number (CharField): The phone number of the architect, must be unique.
        address (CharField): The address of the architect.
        architect_identifier (CharField): Identifier code specific to the architect.
        email (EmailField): The email address of the architect.
        architect_speciality (ForeignKey): The specialty of the architect, linked to the ArchitectSpeciality model.
    """

    first_name = models.CharField(max_length=255, default="")
    last_name = models.CharField(max_length=255, default="")
    phone_number = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=255, default="")
    architect_identifier = models.CharField(max_length=10, default="")
    email = models.EmailField(unique=True)

    architect_speciality = models.ForeignKey(
        ArchitectSpeciality, on_delete=models.CASCADE
    )

    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns the email address of the architect.

        Returns:
            str: The email address of the architect.
        """
        return self.email

    class Meta:
        """
        Meta class for ArchitectRequest model.

        Meta Attributes:
            verbose_name (str): The name of the model in singular form.
            verbose_name_plural (str): The name of the model in plural form.
        """

        verbose_name = "ArchitectRequest"
        verbose_name_plural = "ArchitectRequests"
