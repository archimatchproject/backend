from django.db import models
from app.users.models.ArchimatchUser import ArchimatchUser
from app.models import BaseModel
from app.users.models.utils.SocialMedia import SocialMedia


class Supplier(BaseModel):

    address = models.CharField(max_length=255, default="")
    speciality = models.CharField(max_length=255, default="")
    bio = models.TextField(max_length=1000, default="")
    company_name = models.CharField(max_length=255, default="")
    presentation_video = models.FileField(
        upload_to="SupplierVideos/", blank=True, null=True
    )
    type = models.TextField(max_length=1000, default="")
    social_links = models.OneToOneField(
        SocialMedia, blank=True, null=True, on_delete=models.CASCADE
    )
    user = models.OneToOneField(ArchimatchUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email
