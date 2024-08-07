"""
Module for Announcement ViewSet.

This module defines the AnnouncementViewSet class, which is a viewset
for viewing and editing Announcement instances using Django REST Framework.
"""

from rest_framework import viewsets
from rest_framework.decorators import action

from app.announcement.models import Announcement
from app.announcement.serializers import AnnouncementSerializer
from app.announcement.serializers.AnnouncementSerializer import AnnouncementPOSTSerializer
from app.announcement.serializers.AnnouncementSerializer import AnnouncementPUTSerializer
from app.announcement.serializers.ArchitectSpecialitySerializer import ArchitectSpecialitySerializer
from app.announcement.serializers.ArchitecturalStyleSerializer import ArchitecturalStyleSerializer
from app.announcement.serializers.NeedSerializer import NeedSerializer
from app.announcement.serializers.PieceRenovateSerializer import PieceRenovateSerializer
from app.announcement.serializers.ProjectCategorySerializer import ProjectCategorySerializer
from app.announcement.serializers.ProjectExtensionSerializer import ProjectExtensionSerializer
from app.announcement.serializers.PropertyTypeSerializer import PropertyTypeSerializer
from app.announcement.serializers.WorkTypeSerializer import WorkTypeSerializer
from app.announcement.services import AnnouncementService


class AnnouncementViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Announcement model.

    Provides endpoints for viewing and editing Announcement instances.
    """

    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

    @action(
        detail=False,
        url_path="create-announcement",
        methods=["POST"],
        serializer_class=AnnouncementPOSTSerializer,
    )
    def create_announcement(self, request):
        """
        Creating new announcement
        """
        return AnnouncementService.create_announcement(request.data)

    @action(
        detail=True,
        url_path="update-announcement",
        methods=["PUT"],
        serializer_class=AnnouncementPUTSerializer,
    )
    def update_announcement(self, request, pk=None):
        """
        Updating existing announcement
        """
        instance = self.get_object()
        return AnnouncementService.update_announcement(instance, request.data)

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[],
        url_path="architect-specialities",
        serializer_class=ArchitectSpecialitySerializer,
    )
    def get_architect_specialities(self, request):
        """
        Retrieves all architect specialities.

        Args:
            request (Request): HTTP request object.

        Returns:
            Response: Response containing list of architect specialities.
        """
        return AnnouncementService.get_architect_specialities()

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[],
        url_path="architect-speciality-needs/(?P<architect_speciality_id>[^/.]+)",
        serializer_class=NeedSerializer,
    )
    def get_architect_speciality_needs(self, request, architect_speciality_id):
        """
        Retrieves needs based on architect speciality.

        Args:
            request (Request): HTTP request object.
            architect_speciality_id (int): ID of the architect speciality.

        Returns:
            Response: Response containing list of needs related to the architect speciality.
        """
        return AnnouncementService.get_architect_speciality_needs(architect_speciality_id)

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[],
        url_path="project-categories",
        url_name="project-categories",
        serializer_class=ProjectCategorySerializer,
    )
    def get_project_categories(self, request):
        """
        Retrieves all project categories.

        Args:
            request (Request): HTTP request object.

        Returns:
            Response: Response containing list of project categories.
        """
        return AnnouncementService.get_project_categories()

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[],
        url_path="property-types/(?P<project_category_id>[^/.]+)",
        url_name="property-types",
        serializer_class=PropertyTypeSerializer,
    )
    def get_property_types(self, request, project_category_id):
        """
        Retrieves property types based on project category.

        Args:
            request (Request): HTTP request object.
            project_category_id (int): ID of the project category.

        Returns:
            Response: Response containing list of property types related to the project category.
        """
        return AnnouncementService.get_property_types(project_category_id)

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[],
        url_path="work-types",
        url_name="work-types",
        serializer_class=WorkTypeSerializer,
    )
    def get_announcement_work_types(self, request):
        """
        Retrieves all announcement work types.

        Args:
            request (Request): HTTP request object.

        Returns:
            Response: Response containing list of announcement work types.
        """
        return AnnouncementService.get_announcement_work_types()

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[],
        url_path="renovation-pieces",
        url_name="renovation-pieces",
        serializer_class=PieceRenovateSerializer,
    )
    def get_renovation_pieces(self, request):
        """
        Retrieves all renovation pieces.

        Args:
            request (Request): HTTP request object.

        Returns:
            Response: Response containing list of renovation pieces.
        """
        return AnnouncementService.get_renovation_pieces()

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[],
        url_path="cities",
        url_name="cities",
    )
    def get_cities(self, request):
        """
        Retrieves predefined cities choices.

        Args:
            request (Request): HTTP request object.

        Returns:
            Response: Response containing list of cities.
        """
        return AnnouncementService.get_cities()

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[],
        url_path="terrain-surfaces",
        url_name="terrain-surfaces",
    )
    def get_terrain_surfaces(self, request):
        """
        Retrieves predefined terrain surfaces choices.

        Args:
            request (Request): HTTP request object.

        Returns:
            Response: Response containing list of terrain surfaces.
        """
        return AnnouncementService.get_terrain_surfaces()

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[],
        url_path="work-surfaces",
        url_name="work-surfaces",
    )
    def get_work_surfaces(self, request):
        """
        Retrieves predefined work surfaces choices.

        Args:
            request (Request): HTTP request object.

        Returns:
            Response: Response containing list of work surfaces.
        """
        return AnnouncementService.get_work_surfaces()

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[],
        url_path="budgets",
        url_name="budgets",
    )
    def get_budgets(self, request):
        """
        Retrieves predefined budgets choices.

        Args:
            request (Request): HTTP request object.

        Returns:
            Response: Response containing list of budgets.
        """
        return AnnouncementService.get_budgets()

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[],
        url_path="architectural-styles",
        url_name="architectural-styles",
        serializer_class=ArchitecturalStyleSerializer,
    )
    def get_architectural_styles(self, request):
        """
        Retrieves all architectural styles.

        Args:
            request (Request): HTTP request object.

        Returns:
            Response: Response containing list of architectural styles.
        """
        return AnnouncementService.get_architectural_styles()

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[],
        url_path="project-extensions",
        url_name="project-extensions",
        serializer_class=ProjectExtensionSerializer,
    )
    def get_project_extensions(self, request):
        """
        Retrieves all project extensions.

        Args:
            request (Request): HTTP request object.

        Returns:
            Response: Response containing list of project extensions.
        """
        return AnnouncementService.get_project_extensions()
