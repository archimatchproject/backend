from django.db import models
from app.users.models.ArchimatchUser import ArchimatchUser
from app.utils.models import BaseModel
from app.users.models.utils.SocialMedia import SocialMedia
from app.users.models.utils.SupplierSpeciality import SupplierSpeciality
from app.users.models.utils.SupplierAppearances import APPEARANCES

class Supplier(BaseModel):

    company_address = models.CharField(max_length=255, default="")
    company_speciality = models.CharField(max_length=255, default="")
    bio = models.TextField(max_length=1000, default="")
    company_name = models.CharField(max_length=255, default="")
    presentation_video = models.FileField(
        upload_to="SupplierVideos/", blank=True, null=True
    )
    speciality_type = models.ManyToManyField(SupplierSpeciality, related_name='suppliers')
    appearance = models.CharField(max_length=10, choices=APPEARANCES,default='Petite')
    social_links = models.OneToOneField(
        SocialMedia, blank=True, null=True, on_delete=models.CASCADE
    )
    user = models.OneToOneField(ArchimatchUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email
    
    def delete(self, *args, **kwargs):
        self.user.delete() 
        super().delete(*args, **kwargs)
