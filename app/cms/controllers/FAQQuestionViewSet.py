"""
Module defining the FAQQuestionViewSet.

This module contains the FAQQuestionViewSet class, which provides
view-level logic for the FAQQuestion model, including creation and update operations.
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from app.cms.controllers.ManageFAQPermission import ManageFAQPermission
from app.cms.models.FAQQuestion import FAQQuestion
from app.cms.serializers.FAQQuestionSerializer import FAQQuestionSerializer
from app.cms.services.FAQQuestionService import FAQQuestionService


class FAQQuestionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the FAQQuestion model.

    This class provides view-level logic for the FAQQuestion model,
    including creation and update operations, delegating the business logic
    to the FAQQuestionService.
    """

    queryset = FAQQuestion.objects.all()
    serializer_class = FAQQuestionSerializer

    def get_permissions(self):
        """
        Get the permissions that the view requires.

        For `list` and `retrieve` actions (`GET` requests), no specific permissions are required.
        For `create`, `update`, `partial_update`, and `destroy` actions
        (`POST`, `PUT`, `PATCH`, `DELETE` requests),
        the view requires `IsAuthenticated` and `ManageBlogPermission` permissions.

        Returns:
            list: List of permission instances.
        """
        if self.action in ["list", "retrieve"]:
            return []
        elif self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), ManageFAQPermission()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        """
        Handle the creation of a new FAQQuestion instance along with related FAQQuestion instances.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response object containing the created instance data.
        """
        return FAQQuestionService.create_faq_question(request)

    def update(self, request, *args, **kwargs):
        """
        Handle the update of an existing FAQQuestion instance along with related
        FAQQuestion instances.

        Args:
            request (Request): The request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The response object containing the updated instance data.
        """
        return FAQQuestionService.update_faq_question(self.get_object(), request)
