from django.db import models


class ArchitectType(models.Model):
    display = models.CharField(max_length=255)
    icon = models.ImageField(blank=True, null=True, upload_to="ArchitectTypeIcons/")
    short_def = models.TextField(max_length=1000)

    def __str__(self):
        return self.display
