"""
Module defining the Announcement model.

This module contains the Announcement class, which represents an announcement
for a construction or renovation project in the application.
"""

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from app.announcement import ANNOUNCEMENT_STATUS_CHOICES
from app.announcement import BUDGETS
from app.announcement import CITIES
from app.announcement import PENDING
from app.announcement import TERRAIN_SURFACES
from app.announcement import WORK_SURFACES
from app.announcement.models.Need import Need
from app.announcement.models.ProjectExtension import ProjectExtension
from app.core.models import BaseModel
from app.core.models.ArchitectSpeciality import ArchitectSpeciality
from app.core.models.ArchitecturalStyle import ArchitecturalStyle
from app.core.models.Note import Note
from app.core.models.ProjectCategory import ProjectCategory
from app.core.models.PropertyType import PropertyType
from app.core.models.WorkType import WorkType
from app.users.models.Client import Client

class Announcement(BaseModel):
    """
    Model representing an announcement for a construction or renovation project.

    Attributes:
        client (ForeignKey): Client associated with this announcement.
        architect_speciality (ForeignKey): Specialization of the architect for the project.
        needs (ManyToManyField): Needs or requirements for the project.
        project_category (ForeignKey): Category of the project.
        property_type (ForeignKey): Type of property for the project.
        work_type (ForeignKey): Type of work involved in the project.
        pieces_renovate (ManyToManyField): Pieces or areas to be renovated in the project.
        address (CharField): Address where the project will take place, maximum length of 255
        characters.
        city (CharField): City where the project will take place, selected from predefined
        choices.
        terrain_surface (CharField): Surface type of the terrain for the project, selected from
        predefined choices.
        work_surface (CharField): Surface type where work will be performed, selected from
        predefined choices.
        budget (CharField): Budget range for the project, selected from predefined choices.
        description (TextField): Description of the project.
        architectural_style (CharField): Architectural style preferred for the project,
        selected from predefined choices.
        project_extensions (ManyToManyField): Extensions or additional features
        planned for the project.

    """

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    architect_speciality = models.ForeignKey(
        ArchitectSpeciality,
        on_delete=models.CASCADE,
    )
    needs = models.ManyToManyField(Need, related_name="needs_announcements")
    project_category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE)
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE)
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
    budget = models.CharField(
        max_length=50,
        choices=BUDGETS,
        default=BUDGETS[0],
    )
    description = models.TextField()
    architectural_style = models.ForeignKey(
        ArchitecturalStyle,
        on_delete=models.SET_NULL,
        related_name="architectural_style",
        null=True,
        blank=True,
    )
    project_extensions = models.ManyToManyField(
        ProjectExtension, related_name="project_extensions_announcements"
    )
    number_floors = models.PositiveIntegerField(default=0)
    notes = GenericRelation(Note)
    status = models.CharField(max_length=20, choices=ANNOUNCEMENT_STATUS_CHOICES, default=PENDING)
    admin_note = models.CharField(max_length=500, null=True, blank=True)
    architect = models.ForeignKey("users.Architect", on_delete=models.CASCADE,null=True, blank=True)
    def __str__(self):
        """
        Return a string representation of the announcement.

        Returns:
            str: String representation of the announcement, including its ID and associated client.
        """
        return f"Announcement {self.id} for {self.client}"

    class Meta:
        """
        Meta class for Announcement model.

        Defines display names in the Django admin and plural form of the model name.
        """

        verbose_name = "Announcement"
        verbose_name_plural = "Announcements"
