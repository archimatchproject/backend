"""
Service module for the SubscriptionPlan model.

This module defines the service for handling the business logic and exceptions
related to SubscriptionPlan creation and management.

Classes:
    TokenPackService: Service class for TokenPack operations.
"""

from django.db import transaction

from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from app.subscription.models.TokenPack import TokenPack
from app.users.models.Architect import Architect


class TokenPackService:
    """
    Service class for handling TokenPack operations.

    Handles business logic and exception handling for TokenPack creation and management.
    """

    @classmethod
    def architect_choose_token_pack(cls, request):
        """
        Handles the selection of a TokenPack for an architect, updating the architect's
        subscription plan with additional tokens.

        Args:
            request (Request): The HTTP request object containing user data and token pack ID.

        Returns:
            Response: The response object containing the result of the operation.

        Raises:
            NotFound: If the token pack ID is not provided or the token pack does not exist.
            serializers.ValidationError: If there are validation errors during the process.
            APIException: For any other errors during the process.
        """

        user_id = request.user.id
        token_pack_id = request.data.get("token_pack_id", False)
        if not token_pack_id:
            raise NotFound(detail="Token pack is required")
        try:
            with transaction.atomic():
                token_pack = TokenPack.objects.get(id=token_pack_id)
                architect = Architect.objects.get(user__id=user_id)
                current_plan = architect.subscription_plan
                current_plan.remaining_tokens += token_pack.number_tokens + token_pack.number_free_tokens
                current_plan.save()
                architect.save()
                return Response(
                    {"message": "Token pack is successfully chosen"},
                    status=status.HTTP_200_OK,
                )
        except TokenPack.DoesNotExist:
            raise NotFound(detail="Token pack with this ID is not found")
        except NotFound as e:
            raise e
        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error updating subscription plan: {str(e)}")
