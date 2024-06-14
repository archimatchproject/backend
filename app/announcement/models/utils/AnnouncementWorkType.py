from django.db import models

class AnnouncementWorkType(models.Model):
    header = models.CharField(max_length=255,default='')
    description = models.CharField(max_length=255,default='')


    def __str__(self) -> str:
        return self.header