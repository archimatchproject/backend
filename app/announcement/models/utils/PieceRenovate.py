from django.db import models
from app.utils.models import LabeledIcon

class PieceRenovate(LabeledIcon):
    number = models.PositiveSmallIntegerField(default=0)
