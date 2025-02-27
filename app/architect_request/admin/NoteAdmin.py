"""
Module: app.admin

Class: NoteAdmin

Description:
    Admin configuration for the Note model. Registers the Note model with
    the Django admin interface.
"""

from django.contrib import admin

from app.core.models.Note import Note


class NoteAdmin(admin.ModelAdmin):
    """
    Note configuration for the Note model.
    """

    model = Note


admin.site.register(Note, NoteAdmin)
