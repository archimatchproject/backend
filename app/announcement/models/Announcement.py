from django.db import models

from app.announcement.models.utils.AnnouncementWorkType import AnnouncementWorkType
from app.announcement.models.utils.ArchitectSpeciality import ArchitectSpeciality
from app.announcement.models.utils.ArchitecturalStyles import ARCHITECTURAL_STYLES
from app.announcement.models.utils.Budgets import BUDGETS
from app.announcement.models.utils.Cities import CITIES
from app.announcement.models.utils.Need import Need
from app.announcement.models.utils.PieceRenovate import PieceRenovate
from app.announcement.models.utils.ProjectCategory import ProjectCategory
from app.announcement.models.utils.ProjectExtension import ProjectExtension
from app.announcement.models.utils.ProjectImage import ProjectImage
from app.announcement.models.utils.PropertyType import PropertyType
from app.announcement.models.utils.TerrainSurfaces import TERRAIN_SURFACES
from app.announcement.models.utils.WorkSurfaces import WORK_SURFACES
from app.users.models import Client
from app.utils.models import BaseModel


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
        address (CharField): Address where the project will take place, maximum length of 255 characters.
        city (CharField): City where the project will take place, selected from predefined choices.
        terrain_surface (CharField): Surface type of the terrain for the project, selected from predefined choices.
        work_surface (CharField): Surface type where work will be performed, selected from predefined choices.
        budget (CharField): Budget range for the project, selected from predefined choices.
        description (TextField): Description of the project.
        architectural_style (CharField): Architectural style preferred for the project, selected from predefined choices.
        project_extensions (ManyToManyField): Extensions or additional features planned for the project.
        project_images (ManyToManyField): Images related to the project, optional.

    Methods:
        __str__(): Returns a string representation of the announcement.
    """

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    architect_speciality = models.ForeignKey(
        ArchitectSpeciality, on_delete=models.CASCADE
    )
    needs = models.ManyToManyField(Need, related_name="announcements")
    project_category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE)
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE)
    work_type = models.ForeignKey(AnnouncementWorkType, on_delete=models.CASCADE)
    pieces_renovate = models.ManyToManyField(
        PieceRenovate, related_name="announcements"
    )
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50, choices=CITIES)
    terrain_surface = models.CharField(max_length=50, choices=TERRAIN_SURFACES)
    work_surface = models.CharField(max_length=50, choices=WORK_SURFACES)
    budget = models.CharField(max_length=50, choices=BUDGETS)
    description = models.TextField()
    architectural_style = models.CharField(max_length=50, choices=ARCHITECTURAL_STYLES)
    project_extensions = models.ManyToManyField(
        ProjectExtension, related_name="announcements"
    )
    project_images = models.ManyToManyField(
        ProjectImage, related_name="announcements", blank=True
    )

    def __str__(self):
        return f"Announcement {self.id} for {self.client}"
