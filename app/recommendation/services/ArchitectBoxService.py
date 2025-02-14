"""
Module: announcement Service

This module defines the AnnouncementService class that handles announcement-related operations .

Classes:
    AnnouncementService: Service class for announcement-related operations.

"""

from app.core.pagination import CustomPagination
from app.announcement.models.Announcement import Announcement
from app.recommendation.services.recommend_architects import compute_architect_score
from app.announcement.serializers.AnnouncementSerializer import AnnouncementSerializer
from app.recommendation.models.ArchitectBox import ArchitectBox
from app.users.models.Architect import Architect


class ArchitectBoxService:
    """
    Service class for handling announcement-related operations .

    """

    pagination_class = CustomPagination

    @classmethod
    def recommend_announcements(cls, request):
        """
        Handle GET request and return paginated Announcement objects.

        This method retrieves all Announcement objects from the database, applies
        pagination based on the parameters in the request, and returns the paginated
        results. If the pagination is not applied correctly, it returns a 400 Bad Request response.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Response: A paginated response containing Announcement objects or an error message.
        """
        result = compute_architect_score(
            projet=Announcement.objects.get(id=37),
            attributes=[
                "architectural_style",
                "work_type",
                "project_category",
                "property_type",
            ],
            many_to_many_fields=["needs"],
            weights={
                "distance": 25,
                "perfect_match": 5,
                "architectural_style": 10,
                "work_type": 8,
                "project_category": 6,
                "needs_per_match": 2,
                "on_going_projects": 5,
                "property_type": 5,
            },
            distance_limit=200,
            score_percentage=40,
            num_results=30,
            attribute_mapping={
                "architectural_style": "architectural_styles",
                "work_type": "work_types",
                "project_category": "project_categories",
                "needs": "needs",
                "property_type": "property_types",
            },
        )

        return True, result

    @classmethod
    def get_box_announcements(cls, user):
        """
        Handle GET request and return announcements from the architect's box.

        Args:
            request (HttpRequest): The incoming HTTP request.
            architect_id (int): The ID of the architect.

        Returns:
            Response: A response containing announcements or an error message.
        """
        architect = Architect.objects.get(user=user)
        architect_box = ArchitectBox.objects.get(architect_id=architect.id)
        announcements = architect_box.announcements.all()
        serializer = AnnouncementSerializer(announcements, many=True)
        return True, serializer.data
