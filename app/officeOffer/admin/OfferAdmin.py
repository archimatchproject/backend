"""
Module for custom admin configurations for the Offer model.

This module contains the OfferAdmin class for customizing
the Django admin interface for the Offer model.
"""

from django.contrib import admin

from app.officeOffer.models import Offer


class OfferAdmin(admin.ModelAdmin):
    """
    Custom admin options for Offer model.

    This class provides customizations for the admin interface of
    the Offer model in the Django admin site.
    """

    model = Offer


# Register the admin class with the Offer model
admin.site.register(Offer, OfferAdmin)
