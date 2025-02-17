"""
Module: Office Filters

This module defines the filter classes used to filter Office instances
based on various criteria related to the user and other related fields.
It uses the django_filters library to facilitate the filtering process.

Classes:
    OfficeFilter: FilterSet class for filtering Office instances based on related
    user fields and speciality type.
"""

import django_filters

from app.users.models.Office import Office


class OfficeFilter(django_filters.FilterSet):
    """
    FilterSet class for filtering Office instances based on office name,
    office address, user email, and office name existence.

    This class allows filtering of Office objects based on the following fields:
    - Email: Filters offices by the email address of the related user using
      a case-insensitive contains lookup.
    - Office Name: Filters offices by the office name using a case-insensitive contains lookup.
    - Office Address: Filters offices by the office address using a case-insensitive contains
      lookup.
    - Profile Image Existence: Filters offices based on whether the profile_image
      is empty or not.
    """

    email = django_filters.CharFilter(field_name="user__email", lookup_expr="icontains")

    office_name = django_filters.CharFilter(field_name="office_name", lookup_expr="icontains")
    office_address = django_filters.CharFilter(field_name="office_address", lookup_expr="icontains")

    profile_image_exists = django_filters.BooleanFilter(method="filter_profile_image_exists")

    class Meta:
        """
        Meta class for OfficeFilter.
        """

        model = Office
        fields = [
            "office_name",
            "email",
            "office_address",
            "profile_image_exists",
        ]

    def filter_queryset(self, queryset):
        """
        Filters the given queryset by ordering it based on the 'created_at' field.
        Args:
          queryset (QuerySet): The initial queryset to be filtered.
        Returns:
          QuerySet: The filtered queryset ordered by 'created_at'.
        """

        queryset = queryset.order_by("created_at")
        return super().filter_queryset(queryset)

    def filter_profile_image_exists(self, queryset, name, value):
        """
        Custom filter method to filter offices based on the existence of profile_image.
        If value is True, include offices with non-empty profile_image.
        If value is False, include offices with empty or null profile_image.
        """
        if value:
            return queryset.exclude(profile_image="").order_by("created_at")
        return queryset.filter(profile_image="").order_by("created_at")
