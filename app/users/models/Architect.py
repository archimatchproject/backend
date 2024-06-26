"""
Module containing the Architect model.

This module defines the Architect model, which includes additional fields and relationships
specific to architects within the Archimatch application.

Classes:
    Architect: Define the Architect model with additional fields and relationships.
"""

from django.db import models

from app.core.models import BaseModel
from app.core.models.ArchitectSpeciality import ArchitectSpeciality
from app.users.models.ArchimatchUser import ArchimatchUser
from app.users.models.ArchitectPreferences import (
    BudgetType,
    HouseType,
    LocationType,
    ServiceType,
    WorkSurfaceType,
    WorkType,
)


class Architect(BaseModel):
    """
    Define the Architect model with additional fields and relationships.

    Fields:
        user (OneToOneField): The associated user for this architect, linked one-to-one to an ArchimatchUser instance.
        address (CharField): The address of the architect.
        arch_identifier (CharField): Identifier code specific to the architect.
        arch_type (ForeignKey): The type of architect, selected from a predefined list of ArchitectType choices.
        bio (TextField): Biography or description of the architect.
        company_name (CharField): The name of the company or firm associated with the architect.
        company_logo (ImageField): Logo representing the architect's company or firm, if available.
        first_cnx (BooleanField): Indicates whether the architect has completed their first connection or interaction.
        presentation_video (FileField): Video presentation file uploaded by the architect, if any.
        work_types (ManyToManyField): Types of work the architect specializes in.
        house_types (ManyToManyField): Types of houses or buildings the architect works with.
        services (ManyToManyField): Services offered by the architect.
        locations (ManyToManyField): Locations where the architect operates or provides services.
        work_surfaces (ManyToManyField): Types of work surfaces or materials the architect uses.
        budgets (ManyToManyField): Budget ranges the architect typically works within.
    """

    user = models.OneToOneField(ArchimatchUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, default="")
    architect_identifier = models.CharField(max_length=10, default="")
    architect_speciality = models.ForeignKey(
        ArchitectSpeciality, on_delete=models.CASCADE
    )
    bio = models.TextField(max_length=1000, default="")
    company_name = models.CharField(max_length=255, default="")
    company_logo = models.ImageField(blank=True, null=True, upload_to="CompanyLogos/")
    presentation_video = models.FileField(
        upload_to="ArchitectVideos/", blank=True, null=True
    )

    # preferences
    work_types = models.ManyToManyField(WorkType)
    house_types = models.ManyToManyField(HouseType)
    services = models.ManyToManyField(ServiceType)
    locations = models.ManyToManyField(LocationType)
    work_surfaces = models.ManyToManyField(WorkSurfaceType)
    budgets = models.ManyToManyField(BudgetType)

    def __str__(self):
        """
        Returns the email address of the associated user.

        Returns:
            str: The email address of the user.
        """
        return self.user.email

    class Meta:
        """
        Meta class for Architect model.

        Meta Attributes:
            verbose_name (str): The name of the model in singular form.
            verbose_name_plural (str): The name of the model in plural form.
        """

        verbose_name = "Architect"
        verbose_name_plural = "Architects"
