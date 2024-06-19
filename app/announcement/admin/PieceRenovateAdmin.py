from django.contrib import admin

from app.announcement.models.PieceRenovate import PieceRenovate


class PieceRenovateAdmin(admin.ModelAdmin):
    """
    Admin options for PieceRenovate model.

    This class provides customizations for the admin interface of
    the PieceRenovate model in the Django admin site.

    Attributes:
        list_display (tuple): Specifies the fields to display in the list view of the admin interface.
        search_fields (tuple): Specifies the fields that can be searched in the admin interface.

    Methods:
        None
    """

    list_display = ("id", "label", "icon", "number")
    search_fields = ("label",)


# Register the admin class with the PieceRenovate model
admin.site.register(PieceRenovate, PieceRenovateAdmin)
