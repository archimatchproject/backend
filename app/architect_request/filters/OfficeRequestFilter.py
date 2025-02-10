"""
Module containing the OfficeRequestFilter class.

This module defines the filter class for filtering OfficeRequest objects
based on their status and the email of the Admin responsible for the meeting.

Classes:
    OfficeRequestFilter: Defines the filter class to filter OfficeRequest
    objects based on their status and the meeting_responsable's email.
"""

import django_filters
from app.architect_request.models.OfficeRequest import OfficeRequest


class OfficeRequestFilter(django_filters.FilterSet):
    """
    Filter class for OfficeRequest model to filter by status and meeting_responsable's email.

    Filters:
        - status: Filters OfficeRequest based on their status.
        - meeting_responsable__user__email: Filters OfficeRequest based on the Admin's email
          who is responsible for the meeting.
    """

    status = django_filters.CharFilter(field_name="status", lookup_expr="icontains")
    meeting_responsable_email = django_filters.CharFilter(
        field_name="meeting_responsable__user__email", lookup_expr="icontains"
    )

    class Meta:
        model = OfficeRequest
        fields = ["status", "meeting_responsable_email"]
