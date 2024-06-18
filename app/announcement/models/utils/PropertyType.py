from django.db import models
from .LabeledIcon import LabeledIcon
from .ProjectCategory import ProjectCategory
class PropertyType(LabeledIcon):
    project_category = models.ForeignKey(ProjectCategory, related_name='property_types', on_delete=models.CASCADE,default=None)
