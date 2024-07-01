"""
Module: app.admin

Class: ArchimatchUserAdmin

Description:
    Admin configuration for the ArchimatchUser model. Registers the ArchimatchUser model with the
    Django admin interface
    and defines how the user data is displayed and managed.

"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from app.users.models import ArchimatchUser


class ArchimatchUserAdmin(UserAdmin):
    """
    Admin configuration for the ArchimatchUser model.
    """

    model = ArchimatchUser

    list_display = (
        "email",
        "username",
        "image",
        "phone_number",
        "user_type",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "username",
                    "password",
                    "image",
                    "phone_number",
                    "user_type",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "image",
                    "user_type",
                    "phone_number",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )


admin.site.register(ArchimatchUser, ArchimatchUserAdmin)
