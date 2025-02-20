"""
Module: announcement Service

This module defines the AnnouncementService class that handles announcement-related operations .

Classes:
    AnnouncementService: Service class for announcement-related operations.

"""

from app.announcement.models.Announcement import Announcement
from app.announcement.serializers.AnnouncementSerializer import AnnouncementSerializer
from app.core.pagination import CustomPagination
from app.recommendation.models.ArchitectBox import ArchitectBox
from app.recommendation.models.RecommendationSettings import RecommendationSettings
from app.recommendation.services.recommend_architects import compute_architect_score
from app.users.models.Architect import Architect


class ArchitectBoxService:
    """
    Service class for handling announcement-related operations .

    """

    pagination_class = CustomPagination

    @classmethod
    def compute_score(cls, request, id):
        """
        Handle GET request and return paginated Announcement objects based on recommendation
        settings.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            tuple: (bool, list) Success flag and computed recommendations.
        """
        settings = RecommendationSettings.get_instance()
        attributes = settings.attributes

        result = compute_architect_score(
            projet=Announcement.objects.get(id=id),
            attributes=[
                "architectural_style",
                "work_type",
                "project_category",
                "property_type",
            ],
            many_to_many_fields=["needs"],
            weights={
                "distance": settings.distance,
                "perfect_match": settings.perfect_match,
                "architectural_style": attributes.architectural_style,
                "work_type": attributes.work_type,
                "project_category": attributes.project_category,
                "needs_per_match": attributes.needs_per_match,
                "on_going_projects": settings.on_going_projects,
                "property_type": attributes.property_type,
            },
            distance_limit=settings.distance_limit,
            score_percentage=settings.score_percentage,
            num_results=settings.num_results,
            attribute_mapping={
                "architectural_style": "architectural_styles",
                "work_type": "work_types",
                "project_category": "project_categories",
                "needs": "needs",
                "property_type": "property_types",
            },
        )

        return True, len(result)

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
