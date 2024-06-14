from django.db import models
from app.utils.models import BaseModel
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
from app.announcement.models.utils.AnnouncementWorkType import AnnouncementWorkType
from app.users.models import Client

class Announcement(BaseModel):
    client = models.ForeignKey(Client,on_delete=models.CASCADE)
    architect_speciality = models.ForeignKey(ArchitectSpeciality, on_delete=models.CASCADE)
    needs = models.ManyToManyField(Need, related_name='announcements')
    project_category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE)
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE)
    work_type = models.ForeignKey(AnnouncementWorkType, on_delete=models.CASCADE)
    pieces_renovate = models.ManyToManyField(PieceRenovate, related_name='announcements')
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50, choices=CITIES)
    terrain_surface = models.CharField(max_length=50, choices=TERRAIN_SURFACES)
    work_surface = models.CharField(max_length=50, choices=WORK_SURFACES)
    budget = models.CharField(max_length=50, choices=BUDGETS)
    description = models.TextField()
    architectural_style = models.CharField(max_length=50, choices=ARCHITECTURAL_STYLES)
    project_extensions = models.ManyToManyField(ProjectExtension, related_name='announcements')
    project_images = models.ManyToManyField(ProjectImage, related_name='announcements', blank=True)
    

    def __str__(self):
        return f"Announcement {self.id} for {self.client}"
