from django.db import models


class Preference(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


# Define choice model names
CHOICE_MODEL_NAMES = [
    "WorkType",
    "HouseType",
    "ServiceType",
    "LocationType",
    "WorkSurfaceType",
    "BudgetType",
]

# Dynamically create choice models inheriting from Preference
for model_name in CHOICE_MODEL_NAMES:
    # Dynamically create the model class
    globals()[model_name] = type(model_name, (Preference,), {"__module__": __name__})
