from django.db import models
from .LabeledIcon import LabeledIcon
from .ArchitectSpeciality import ArchitectSpeciality
class Need(LabeledIcon):
    architect_speciality = models.ForeignKey(ArchitectSpeciality, related_name='needs', on_delete=models.CASCADE,default=None)
