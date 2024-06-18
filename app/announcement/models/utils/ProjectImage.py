from django.db import models
from django.core.exceptions import ValidationError
class ProjectImage(models.Model):
    image = models.ImageField(upload_to='images/')

    def clean(self):
        if self.project.images.count() >= 5:
            raise ValidationError('A gallery can contain a maximum of 5 images.')

    def __str__(self):
        return f"Image {self.id} for {self.project.client}"