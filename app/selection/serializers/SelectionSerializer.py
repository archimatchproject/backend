"""
This module contains serializers for the Selection model, handling the representation
and validation of the Selection data.

Classes:
    SelectionSerializer: Serializes the Selection model and enforces validation rules.
"""

from django.utils.timezone import now

from rest_framework import serializers

from app.announcement.models import Announcement
from app.announcement.serializers.AnnouncementSerializer import AnnouncementSerializer
from app.selection import QUOTE_ACCEPTED
from app.selection import QUOTE_PENDING
from app.selection import QUOTE_REFUSED
from app.selection import SELECTION_STATUS_CHOICES
from app.selection.models.Selection import Selection
from app.selection.serializers.PhaseSerializer import PhaseSerializer
from app.selection.serializers.QuoteSerializer import QuoteSerializer
from app.users.models import Architect
from app.users.serializers.ArchitectSerializer import ArchitectSerializer


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
    is_last_quote_accepted = serializers.SerializerMethodField()
    is_last_quote_refused = serializers.SerializerMethodField()
    last_pending_quote = serializers.SerializerMethodField()
    days_remaining = serializers.SerializerMethodField()
    admin_management_reached = serializers.SerializerMethodField()

    class Meta:
        """
        Meta class for the SelectionSerializer.
        Attributes:
            model (Model): The model that is being serialized.
            fields (list): A list of fields to be included in the serialization.
                - id (int): The unique identifier for the selection.
                - announcement (str): The announcement related to the selection.
                - architect (str): The architect associated with the selection.
                - phase (str): The current phase of the selection.
                - status (str): The status of the selection.
                - quotes (list): A list of quotes related to the selection.
                - is_last_quote_accepted (bool): Indicates if the last quote was accepted.
                - is_last_quote_refused (bool): Indicates if the last quote was refused.
                - name (str): The name of the selection.
                - last_pending_quote (str): The last pending quote for the selection.
                - is_client_interested (bool): Indicates if the client is interested.
                - days_remaining (int): The number of days remaining for the selection.
                - admin_management_reached (bool): Indicates if admin management has been reached.
                - is_blocked (bool): Indicates if the selection is blocked.
                - is_abandoned (bool): Indicates if the selection is abandoned.
        """

        model = Selection
        fields = [
            "id",
            "announcement",
            "architect",
            "phase",
            "status",
            "quotes",
            "is_last_quote_accepted",
            "is_last_quote_refused",
            "name",
            "last_pending_quote",
            "is_client_interested",
            "days_remaining",
            "admin_management_reached",
            "is_blocked",
            "is_abandoned",
        ]

    def get_is_last_quote_accepted(self, obj):
        """
        Checks if the last quote associated with this selection was accepted.

        Args:
            obj (Selection): The Selection instance.

        Returns:
            bool: True if the last quote's status is 'Accepted'; False otherwise.
        """
        last_quote = obj.quotes.order_by("-created_at").first()
        return last_quote.status == QUOTE_ACCEPTED if last_quote else False

    def get_is_last_quote_refused(self, obj):
        """
        Checks if the last quote associated with this selection was refused.

        Args:
            obj (Selection): The Selection instance.

        Returns:
            bool: True if the last quote's status is 'Refused'; False otherwise.
        """
        last_quote = obj.quotes.order_by("-created_at").first()
        return last_quote.status == QUOTE_REFUSED if last_quote else False

    def get_last_pending_quote(self, obj):
        """
        Retrieves the latest quote with a status of 'pending' for this selection.

        Args:
            obj (Selection): The Selection instance.

        Returns:
            dict: Serialized data of the last 'pending' quote, or None if no pending quote exists.
        """
        last_pending_quote = obj.quotes.filter(status=QUOTE_PENDING).order_by("-created_at").first()
        return QuoteSerializer(last_pending_quote).data if last_pending_quote else None

    def get_days_remaining(self, obj):
        """
        Calculate the remaining days for the end of the phase.

        Args:
            obj (Selection): The Selection instance.

        Returns:
            int: The number of days remaining until the phase's limit_date. Returns None if no
            phase is set.
        """
        if obj.phase and obj.phase.limit_date:
            today = now().date()
            remaining_days = (obj.phase.limit_date - today).days
            return max(0, remaining_days)
        return None

    def get_admin_management_reached(self, obj):
        """
        Determine if the time from created_at to today has reached days_for_admin_management.

        Args:
            obj (Selection): The Selection instance.

        Returns:
            bool: True if the duration since created_at equals or exceeds days_for_admin_management,
            False otherwise.
        """
        selection_settings = self.context.get("selection_settings")
        if selection_settings:
            days_for_admin_management = selection_settings.days_for_admin_management
            created_at = obj.phase.start_date
            today = now().date()
            duration = (today - created_at).days
            return duration >= days_for_admin_management
        return False

    def to_representation(self, instance):
        """
        Customize the representation of the Selection instance.

        Args:
            instance (Selection): The Selection instance.

        Returns:
            dict: The serialized representation of the Selection instance.
        """
        representation = super().to_representation(instance)

        # Get the last pending quote
        last_pending_quote = self.get_last_pending_quote(instance)

        # Remove the last pending quote from the quotes list if it exists
        if last_pending_quote:
            representation["quotes"] = [
                quote for quote in representation["quotes"] if quote["id"] != last_pending_quote["id"]
            ]

        return representation


class SelectionPostSerializer(serializers.ModelSerializer):
    """
    Serializer for creating or updating a Selection with minimal input.

    Fields:
        announcement_id: The ID of the announcement related to the selection.
        architect_id: The ID of the architect interested in the announcement (optional).
        status: The status of the selection (e.g., 'Interested', 'Accepted', 'Rejected').
    """

    announcement = serializers.PrimaryKeyRelatedField(queryset=Announcement.objects.all(), write_only=True)
    architect = serializers.PrimaryKeyRelatedField(queryset=Architect.objects.all(), write_only=True, required=False)

    class Meta:
        """
        Meta class for the SelectionSerializer.
        Attributes:
            model (type): The model that is being serialized.
            fields (list): A list of fields to be included in the serialization.
        """

        model = Selection
        fields = ["announcement", "architect"]


class SelectionPutSerializer(serializers.ModelSerializer):
    """
    Serializer for creating or updating a Selection with minimal input.

    Fields:
        announcement_id: The ID of the announcement related to the selection.
        architect_id: The ID of the architect interested in the announcement (optional).
        status: The status of the selection (e.g., 'Interested', 'Accepted', 'Rejected').
    """

    announcement = serializers.PrimaryKeyRelatedField(queryset=Announcement.objects.all(), write_only=True)
    architect = serializers.PrimaryKeyRelatedField(queryset=Architect.objects.all(), write_only=True, required=False)
    status = serializers.ChoiceField(choices=SELECTION_STATUS_CHOICES, default="interested")

    class Meta:
        """
        Meta class for the SelectionSerializer.
        Attributes:
            model (django.db.models.Model): The model that is being serialized.
            fields (list): A list of fields to be included in the serialized output.
        """

        model = Selection
        fields = ["announcement_id", "architect_id", "status"]
