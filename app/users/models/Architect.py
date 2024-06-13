from django.db import models
from app.users.models.ArchimatchUser import ArchimatchUser
from app.users.models.utils.ArchitectPreferences import (
    WorkType,
    HouseType,
    BudgetType,
    ServiceType,
    LocationType,
    WorkSurfaceType,
)
from app.users.models.ArchitectType import ArchitectType
from app.models import BaseModel


class Architect(BaseModel):
    user = models.OneToOneField(ArchimatchUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, default="")
    arch_identifier = models.CharField(max_length=10, default="")
    arch_type = models.ForeignKey(
        ArchitectType, related_name="architects", on_delete=models.DO_NOTHING
    )
    bio = models.TextField(max_length=1000, default="")
    company_name = models.CharField(max_length=255, default="")
    company_logo = models.ImageField(blank=True, null=True, upload_to="CompanyLogos/")
    first_cnx = models.BooleanField(default=False)
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
        return self.user.email

    class Meta:
        verbose_name_plural = "Architects"
