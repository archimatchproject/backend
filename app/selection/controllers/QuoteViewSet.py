"""
Module: Quote ViewSet

This module defines the `QuoteViewSet`, which provides the API endpoints to manage `Quote` resources 
associated with selections in the selection process.

Classes:
    QuoteViewSet: A viewset that provides the actions for creating and managing quotes.
"""

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from app.selection.services.QuoteService import QuoteService
from app.users.models.Architect import Architect
from django.core.exceptions import ValidationError

class QuoteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling quote-related actions.

    This ViewSet provides the following actions:
    - create_quote: Allows users to upload a PDF quote for a specific selection.

    Attributes:
        - None

    Methods:
        - create_quote: Handles the creation of a new quote for a specific selection.
    """

    @action(detail=True, methods=['POST'], url_path='create-quote')
    def create_quote(self, request, pk=None):
        """
        Handles the creation of a new quote associated with a specific selection.

        This method expects a PDF file to be uploaded in the request, which will be linked to the
        selection specified by the `pk` (selection ID) in the URL.

        Args:
            request (Request): The request object containing the uploaded file.
            pk (int): The ID of the selection for which the quote is being created (extracted from the URL).

        Returns:
            Response: The response object containing the created quote's details if successful, 
                      or an error message if something went wrong.
        
        Raises:
            ValidationError: If the uploaded file is not a PDF or if the file is missing from the request.
        """
        
        file = request.FILES.get('file')
        architect = Architect.objects.get(user=request.user)
        if not file:
            raise ValidationError(detail="File is required.", status=status.HTTP_400_BAD_REQUEST)

        success, data = QuoteService.create_quote(selection_id=pk, file=file,architect=architect)
        return Response(data, status=status.HTTP_201_CREATED, success=success)

    @action(detail=True, methods=['POST'], url_path='accept')
    def accept_quote(self, request, pk=None):
        """
        Endpoint to accept a quote and update the associated selection.

        Args:
            pk (int): The ID of the quote to accept.

        Returns:
            Response: The updated quote and selection data or an error message.
        """

        success, message = QuoteService.accept_quote(quote_id=pk)
        return Response(success=success, message=message, status=status.HTTP_200_OK)
    

    @action(detail=True, methods=['POST'], url_path='refuse')
    def refuse_quote(self, request, pk=None):
        """
        Endpoint to refuse a quote.

        Args:
            pk (int): The ID of the quote to refuse.

        Returns:
            Response: The updated quote data or an error message.
        """
        success, message = QuoteService.refuse_quote(quote_id=pk)
        return Response(success=success, message=message, status=status.HTTP_200_OK)