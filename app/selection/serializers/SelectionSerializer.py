"""
This module contains serializers for the Selection model, handling the representation
and validation of the Selection data.

Classes:
    SelectionSerializer: Serializes the Selection model and enforces validation rules.
"""

from rest_framework import serializers
from app.selection.models.Selection import Selection
from app.selection.serializers.PhaseSerializer import PhaseSerializer
from app.selection.serializers.QuoteSerializer import QuoteSerializer
from app.users.models import Architect
from app.announcement.models import Announcement
from app.announcement.serializers.AnnouncementSerializer import AnnouncementSerializer
from app.users.serializers.ArchitectSerializer import ArchitectSerializer
from app.selection import SELECTION_STATUS_CHOICES


class SelectionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Selection model.

    Fields:
        announcement: The announcement related to the selection.
        architect: The architect interested in the announcement.
        phase: The current phase in the selection process.
        status: The status of the selection (e.g., 'Interested', 'Accepted', 'Rejected').
    """

    announcement = AnnouncementSerializer()
    architect = ArchitectSerializer()
    phase = PhaseSerializer() 
    quotes = QuoteSerializer(many=True, read_only=True)
    class Meta:
        model = Selection
        fields = ['announcement', 'architect', 'phase', 'status','quotes','name']

class SelectionPostSerializer(serializers.ModelSerializer):
    """
    Serializer for creating or updating a Selection with minimal input.

    Fields:
        announcement_id: The ID of the announcement related to the selection.
        architect_id: The ID of the architect interested in the announcement (optional).
        status: The status of the selection (e.g., 'Interested', 'Accepted', 'Rejected').
    """

    announcement = serializers.PrimaryKeyRelatedField(
        queryset=Announcement.objects.all(),
        write_only=True
    )
    architect = serializers.PrimaryKeyRelatedField(
        queryset=Architect.objects.all(),
        write_only=True,
        required=False
    )
    class Meta:
        model = Selection
        fields = ['announcement', 'architect']

    
    

class SelectionPutSerializer(serializers.ModelSerializer):
    """
    Serializer for creating or updating a Selection with minimal input.

    Fields:
        announcement_id: The ID of the announcement related to the selection.
        architect_id: The ID of the architect interested in the announcement (optional).
        status: The status of the selection (e.g., 'Interested', 'Accepted', 'Rejected').
    """

    announcement = serializers.PrimaryKeyRelatedField(
        queryset=Announcement.objects.all(),
        write_only=True
    )
    architect = serializers.PrimaryKeyRelatedField(
        queryset=Architect.objects.all(),
        write_only=True,
        required=False
    )
    status = serializers.ChoiceField(
        choices=SELECTION_STATUS_CHOICES,
        default='interested'
    )

    class Meta:
        model = Selection
        fields = ['announcement_id', 'architect_id', 'status']