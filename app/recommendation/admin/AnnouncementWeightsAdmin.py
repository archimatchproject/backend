"""
Module: app.admin

Classes:
- ArchitectForm: Form class for the Architect model, defining fields and widgets.

- ArchitectAdmin: Admin configuration for the Architect model.

- ArchitectTypeAdmin: Admin configuration for the ArchitectType model.

Description:
This module registers the Architect and ArchitectType models with the Django admin interface
and defines custom forms and configurations for managing these models.

"""

from django.contrib import admin

from app.recommendation.models.AnnouncementWeights import AnnouncementWeights


class AnnouncementWeightsAdmin(admin.ModelAdmin):
    """
    Admin configuration for the AnnouncementWeights model.
    model (type): Specifies the AnnouncementWeights model.
    """

    model = AnnouncementWeights


admin.site.register(AnnouncementWeights, AnnouncementWeightsAdmin)
