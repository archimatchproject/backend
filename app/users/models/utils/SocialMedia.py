from django.db import models

from app.models import BaseModel


class SocialMedia(BaseModel):

    facebook = models.CharField(max_length=255, default="")
    instagram = models.CharField(max_length=255, default="")
    website = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.facebook
