"""
Module: announcement Service

This module defines the AnnouncementService class that handles announcement-related operations .

Classes:
    AnnouncementService: Service class for announcement-related operations.

"""


from django.core.exceptions import ValidationError
from app.selection.models.Selection import Selection
from app.selection.models.Quote import Quote
from rest_framework.exceptions import APIException

from app.selection.serializers.QuoteSerializer import QuoteSerializer
from django.db import transaction
from app.selection import QUOTE_ACCEPTED,QUOTE_REFUSED,ACCEPTED
class QuoteService:
    """
    Service class for handling quote-related operations.
    """

    @classmethod
    def create_quote(cls, selection_id, file,architect):
        """
        Creates a quote associated with a specific selection.

        Args:
            selection_id (int): The ID of the selection for which the quote is being created.
            file (File): The PDF file for the quote.

        Returns:
            tuple: (bool, dict) indicating success and the created quote data.

        Raises:
            APIException: If there are any issues during quote creation.
        """
        

        selection = Selection.objects.get(id=selection_id)
        if selection.architect is not architect :
            raise APIException(detail="you must be the owner of the project to upload a Quote")
        
        cls._validate_pdf_file(file)

        quote = Quote.objects.create(
            selection=selection,
            file=file
        )

        return True, QuoteSerializer(quote).data

    @staticmethod
    def _validate_pdf_file(file):
        """
        Validates that the uploaded file is a PDF.

        Args:
            file (File): The uploaded file to be validated.

        Raises:
            ValidationError: If the file is not a PDF.
        """
        if not file.name.endswith('.pdf'):
            raise ValidationError("Only PDF files are allowed for quotes.")

    
    @classmethod
    @transaction.atomic
    def accept_quote(cls, quote_id):
        """
        Accepts a quote by setting its status to 'Accepted'.

        Args:
            quote_id (int): The ID of the quote to accept.

        Returns:
            tuple: (bool, dict) A success flag and the updated quote data.

        Raises:
            APIException: If the quote is already accepted or there is an issue.
        """
        
        quote = Quote.objects.select_for_update().get(id=quote_id)

        if quote.status == QUOTE_ACCEPTED:
            raise APIException("This quote has already been accepted.")

        quote.status = QUOTE_ACCEPTED
        quote.save()
        selection = quote.selection
        
        if selection.status != ACCEPTED :
            selection.status = ACCEPTED
            selection.save()

        return True, "Quote is accepted"

    @classmethod
    @transaction.atomic
    def refuse_quote(cls, quote_id):
        """
        Refuses a quote by setting its status to 'Refused'.

        Args:
            quote_id (int): The ID of the quote to refuse.

        Returns:
            tuple: (bool, dict) A success flag and the updated quote data.

        Raises:
            APIException: If the quote is already refused or there is an issue.
        """

        quote = Quote.objects.select_for_update().get(id=quote_id)
        
        
        
        if quote.status == QUOTE_REFUSED:
            raise APIException("This quote has already been refused.")

        quote.status = QUOTE_REFUSED
        quote.save()

        # Return success and the updated quote data
        return True, "Quote is accepted"