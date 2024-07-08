"""
Module defining the Realization model.

This module contains the Realization class, which represents a realization
for a construction or renovation project in the application.
"""

from django.db import models

from app.announcement import CITIES
from app.announcement import TERRAIN_SURFACES
from app.announcement import WORK_SURFACES
from app.core.models import BaseModel
from app.core.models.ArchitecturalStyle import ArchitecturalStyle
from app.core.models.ProjectCategory import ProjectCategory
from app.core.models.WorkType import WorkType
from app.users.models.Architect import Architect


class Realization(BaseModel):
    """
    Model representing a realization for a construction or renovation project.

    Attributes:
        architect (ForeignKey): Architect associated with this realization.
        project_category (ForeignKey): Category of the project.
        work_type (ForeignKey): Type of work involved in the project.
        address (CharField): Address where the project will take place, maximum length
        of 255 characters.
        city (CharField): City where the project will take place, selected from
        predefined choices.
        terrain_surface (CharField): Surface type of the terrain for the project,
        selected from predefined choices.
        work_surface (CharField): Surface type where work will be performed,
        selected from predefined choices.
        description (TextField): Description of the project.
        architectural_style (ForeignKey): Architectural style preferred for the project,
        selected from predefined choices.
    """

    architect = models.ForeignKey(Architect, on_delete=models.CASCADE)
    project_category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE)
    work_type = models.ForeignKey(WorkType, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    city = models.CharField(
        max_length=50,
        choices=CITIES,
        default=CITIES[0],
    )
    terrain_surface = models.CharField(
        max_length=50,
        choices=TERRAIN_SURFACES,
        default=TERRAIN_SURFACES[0],
    )
    work_surface = models.CharField(
        max_length=50,
        choices=WORK_SURFACES,
        default=WORK_SURFACES[0],
    )
    description = models.TextField()
    architectural_style = models.ForeignKey(
        ArchitecturalStyle,
        on_delete=models.SET_NULL,
        related_name="realization_architectural_style",
        null=True,
    )

    def __str__(self):
        """
        Return a string representation of the realization.

        Returns:
            str: String representation of the realization, including its ID
            and associated architect.
        """
        return f"Realization {self.id} by {self.architect}"

    class Meta:
        """
        Meta class for Realization model.

        Defines display names in the Django admin and plural form
        of the model name.
        """

        verbose_name = "Realization"
        verbose_name_plural = "Realizations"
