"""
ViewSet module for the TokenPack model.
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from app.subscription.controllers.ManageSubscriptionPermission import ManageSubscriptionPermission
from app.subscription.models.TokenPack import TokenPack
from app.subscription.serializers.TokenPackSerializer import TokenPackSerializer
from app.subscription.services.TokenPackService import TokenPackService
from app.core.exception_handler import handle_service_exceptions
from app.core.response_builder import build_response
from rest_framework import status

class TokenPackViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the TokenPack model.
    """

    queryset = TokenPack.objects.all()
    serializer_class = TokenPackSerializer

    def get_permissions(self):
        """
        Get the permissions that the view requires.

        For `list` and `retrieve` actions (`GET` requests), no specific permissions are required.
        For `create`, `update`, `partial_update`, and `destroy` actions
        (`POST`, `PUT`, `PATCH`, `DELETE` requests),
        the view requires `IsAuthenticated` permissions.

        Returns:
            list: List of permission instances.
        """
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        elif self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), ManageSubscriptionPermission()]
        return super().get_permissions()

    @action(detail=False, methods=["post"], url_path="choose-pack", url_name="choose-pack")
    @handle_service_exceptions
    def architect_choose_token_pack(self, request):
        """
        Custom action to choose a token pack for an architect.

        Args:
            request (Request): The HTTP request object containing user data.

        Returns:
            Response: The response object containing the result of the operation.
        """
        success,message = TokenPackService.architect_choose_token_pack(request)
        return build_response(success=success, message=message, status=status.HTTP_200_OK)

    @handle_service_exceptions
    def list(self, request, *args, **kwargs):
        """
        Create a new SubscriptionPlan instance.

        Args:
            request (Request): The HTTP request object containing data to create
            SubscriptionPlan instance.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: Serialized data of the created SubscriptionPlan instance.
        """
        success,data = TokenPackService.get_all_token_packs()
        return build_response(success=success, data=data, status=status.HTTP_200_OK)