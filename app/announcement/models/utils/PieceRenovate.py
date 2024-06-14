from django.db import models
from .LabeledIcon import LabeledIcon

class PieceRenovate(LabeledIcon):
    number = models.PositiveSmallIntegerField(default=0)
