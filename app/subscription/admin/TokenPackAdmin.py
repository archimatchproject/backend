"""
Admin registration module for the TokenPack model.
"""

from django.contrib import admin

from app.subscription.models.TokenPack import TokenPack


class TokenPackAdmin(admin.ModelAdmin):
    """
    Admin interface for TokenPack.
    """

    list_display = ("pack_name", "pack_price", "number_tokens", "number_free_tokens", "active")
    search_fields = ("pack_name",)
    list_filter = ("active",)


admin.site.register(TokenPack, TokenPackAdmin)
