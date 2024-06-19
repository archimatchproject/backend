from django.db import models

from .LabeledIcon import LabeledIcon


class ProjectCategory(LabeledIcon):
    """
    Model representing a category of project, inheriting from LabeledIcon.

    Inherits:
        LabeledIcon: Base class providing fields for label and icon.

    This class inherits all fields and behavior from LabeledIcon.
    """

    pass
