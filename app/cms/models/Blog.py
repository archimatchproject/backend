from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=255)
    cover_photo = models.ImageField(
        upload_to="BlogsCoverPhotos/", blank=True, null=True
    )

    def __str__(self):
        return self.title
