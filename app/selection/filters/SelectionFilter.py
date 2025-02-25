"""
This module defines a filter set for the Selection model using django_filters.
Classes:
    SelectionFilter: A FilterSet class for filtering Selection instances based on related fields.
Usage:
    Use this filter set to filter Selection instances by their status field using case-insensitive containment lookup.
"""

import django_filters

from app.selection.models.Selection import Selection


class SelectionFilter(django_filters.FilterSet):
    """
    FilterSet class for filtering Selection instances based on related  fields,

    """

    status = django_filters.CharFilter(field_name="status", lookup_expr="icontains")

    class Meta:
        """
        Meta class for the SelectionFilter.
        Attributes:
            model (type): The model class that this filter is associated with.
            fields (list): A list of fields to include in the filter.
        """

        model = Selection
        fields = ["status"]
