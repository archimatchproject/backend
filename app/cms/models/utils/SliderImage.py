from django.db import models
from .Block import Block

class SliderImage(models.Model):
    image = models.ImageField(upload_to='BlockSliderImages/')
    block = models.ForeignKey(Block, related_name='slider_images', on_delete=models.CASCADE,default=None)
    def __str__(self):
        return self.image.url