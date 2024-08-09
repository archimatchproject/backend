"""
Module for Announcement ViewSet.

This module defines the AnnouncementViewSet class, which is a viewset
for viewing and editing Announcement instances using Django REST Framework.
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from app.announcement.models.Announcement import Announcement
from app.announcement.serializers.AnnouncementSerializer import AnnouncementPOSTSerializer
from app.announcement.serializers.AnnouncementSerializer import AnnouncementPUTSerializer
from app.announcement.serializers.AnnouncementSerializer import AnnouncementSerializer
from app.announcement.serializers.ArchitectSpecialitySerializer import ArchitectSpecialitySerializer
from app.announcement.serializers.ArchitecturalStyleSerializer import ArchitecturalStyleSerializer
from app.announcement.serializers.NeedSerializer import NeedSerializer
from app.announcement.serializers.PieceRenovateSerializer import PieceRenovateSerializer
from app.announcement.serializers.ProjectCategorySerializer import ProjectCategorySerializer
from app.announcement.serializers.ProjectExtensionSerializer import ProjectExtensionSerializer
from app.announcement.serializers.PropertyTypeSerializer import PropertyTypeSerializer
from app.announcement.serializers.WorkTypeSerializer import WorkTypeSerializer
from app.announcement.services.AnnouncementService import AnnouncementService
from app.core.serializers.NoteSerializer import NoteSerializer


class AnnouncementViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Announcement model.

    Provides endpoints for viewing and editing Announcement instances.
    """

    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

    def get_permissions(self):
        """
        Return the list of permissions that this view requires.

        Applies different permissions based on the action being executed.

        Returns:
            list: The list of permission classes.
        """
        if self.action in [
            "list",
        ]:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = []
        return super().get_permissions()

    def get_queryset(self):
        """
        Filter the collections by the supplier related to the currently authenticated user.
        """
        user = self.request.user
        return Announcement.objects.filter(client__user=user)

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
        return AnnouncementService.create_announcement(request)

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
        detail=True,
        url_path="update-announcement-images",
        methods=["PUT"],
    )
    def update_announcement_images(self, request, pk=None):
        """
        Updating existing announcement
        """
        instance = self.get_object()
        return AnnouncementService.update_announcement_images(instance, request)

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
        url_path="architect-speciality-needs",
        serializer_class=NeedSerializer,
    )
    def get_architect_speciality_needs(self, request):
        """
        Retrieves needs based on architect speciality.

        Args:
            request (Request): HTTP request object.
            architect_speciality_id (int): ID of the architect speciality.

        Returns:
            Response: Response containing list of needs related to the architect speciality.
        """
        architect_speciality_id = request.query_params.get("architect_speciality_id")
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
        url_path="property-types",
        url_name="property-types",
        serializer_class=PropertyTypeSerializer,
    )
    def get_property_types(self, request):
        """
        Retrieves property types based on project category.

        Args:
            request (Request): HTTP request object.
            project_category_id (int): ID of the project category.

        Returns:
            Response: Response containing list of property types related to the project category.
        """
        project_category_id = request.query_params.get("project_category_id")
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
        property_type_id = request.query_params.get("property_type_id")
        return AnnouncementService.get_announcement_work_types(property_type_id)

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
        property_type_id = request.query_params.get("property_type_id")
        work_type_id = request.query_params.get("work_type_id")
        return AnnouncementService.get_renovation_pieces(property_type_id, work_type_id)

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
        property_type_id = request.query_params.get("property_type_id")
        return AnnouncementService.get_architectural_styles(property_type_id)

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
        property_type_id = request.query_params.get("property_type_id")
        work_type_id = request.query_params.get("work_type_id")
        return AnnouncementService.get_project_extensions(property_type_id, work_type_id)

    @action(
        detail=True,
        methods=["POST"],
        url_path="add-note",
        serializer_class=NoteSerializer,
    )
    def add_note(self, request, pk=None):
        """
        Custom action to add a note to an Announcement.

        Args:
            request (Request): The request object containing the input data.
            pk (str): The primary key of the Announcement to which the note will be added.

        Returns:
            Response: The response object containing the result of the operation.
        """
        return AnnouncementService.add_note_to_announcement(pk, request.data)

    def get(self, request):
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
        return AnnouncementService.get_announcements(request)

    @action(
        detail=True,
        methods=["POST"],
        url_path="accept-announcement",
        serializer_class=NoteSerializer,
    )
    def accept_announcement(self, request, pk=None):
        """
        Custom action to accept an Announcement.

        Args:
            request (Request): The request object containing the input data.
            pk (str): The primary key of the Announcement to be accepted.

        Returns:
            Response: The response object containing the result of the acceptance operation.
        """
        return AnnouncementService.accept_announcement(pk)

    @action(
        detail=True,
        methods=["POST"],
        url_path="refuse-announcement",
        serializer_class=NoteSerializer,
    )
    def refuse_announcement(self, request, pk=None):
        """
        Custom action to refuse an Announcement.

        Args:
            request (Request): The request object containing the input data.
            pk (str): The primary key of the Announcement to be refused.

        Returns:
            Response: The response object containing the result of the refusal operation.
        """
        return AnnouncementService.refuse_announcement(pk)

    @action(
        detail=True,
        methods=["GET"],
        url_path="get-details",
    )
    def get_announcement_details(self, request, pk=None):
        """
        Custom action to refuse an Announcement.

        Args:
            request (Request): The request object containing the input data.
            pk (str): The primary key of the Announcement to be refused.

        Returns:
            Response: The response object containing the result of the refusal operation.
        """
        return AnnouncementService.get_announcement_details(pk)
