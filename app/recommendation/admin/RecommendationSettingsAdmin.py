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

from app.recommendation.models.RecommendationSettings import RecommendationSettings


class RecommendationSettingsAdmin(admin.ModelAdmin):
    """
    Admin configuration for the RecommendationSettings model.

    Attributes:
    - model: Specifies the RecommendationSettings model.

    """

    model = RecommendationSettings


admin.site.register(RecommendationSettings, RecommendationSettingsAdmin)
