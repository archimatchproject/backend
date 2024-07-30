"""
Admin registration module for the Collection model.
"""

from django.contrib import admin

from app.catalogue.models.Collection import Collection


class CollectionAdmin(admin.ModelAdmin):
    """
    Admin interface for Collection.
    """

    list_display = ("title", "category")
    search_fields = ("title", "category__name")


admin.site.register(Collection, CollectionAdmin)
