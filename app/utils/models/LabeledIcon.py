from django.db import models

class LabeledIcon(models.Model):
    label = models.CharField( max_length=255,default='')
    icon = models.ImageField( upload_to='Icons/')

    def __str__(self):
        return self.label
