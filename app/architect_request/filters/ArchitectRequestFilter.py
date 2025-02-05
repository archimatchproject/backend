"""
Module containing the ArchitectRequestFilter class.

This module defines the filter class for filtering ArchitectRequest objects
based on their status and the email of the Admin responsible for the meeting.

Classes:
    ArchitectRequestFilter: Defines the filter class to filter ArchitectRequest
    objects based on their status and the meeting_responsable's email.
"""

import django_filters
from app.architect_request.models import ArchitectRequest

class ArchitectRequestFilter(django_filters.FilterSet):
    """
    Filter class for ArchitectRequest model to filter by status and meeting_responsable's email.

    Filters:
        - status: Filters ArchitectRequest based on their status.
        - meeting_responsable__user__email: Filters ArchitectRequest based on the Admin's email
          who is responsible for the meeting.
    """

    status = django_filters.CharFilter(field_name='status', lookup_expr='icontains')
    meeting_responsable_email = django_filters.CharFilter(
        field_name='meeting_responsable__user__email', 
        lookup_expr='icontains'
    )

    class Meta:
        model = ArchitectRequest
        fields = ['status', 'meeting_responsable_email']
