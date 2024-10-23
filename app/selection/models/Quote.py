"""
Module: Quote Model

This module defines the Quote model, which represents quotes associated with selections in the selection process.

Classes:
    Quote: A model that stores information about quotes linked to selections, including the uploaded PDF file.

Functions:
    validate_pdf_file(value): Validates that the uploaded file is a PDF.

Attributes:
    selection (ForeignKey): A reference to the Selection to which this quote belongs.
    file (FileField): The uploaded PDF file for the quote.
    created_at (DateTimeField): The timestamp when the quote was created (automatically set).
"""

from django.db import models
from app.core.models.BaseModel import BaseModel
from app.selection.models.Selection import Selection 
from app.selection import QUOTE_PENDING,QUOTE_STATUS_CHOICES


class Quote(BaseModel):
    """
    Model representing a quote associated with a selection.

    Attributes:
        id (UUID): The unique identifier for the quote (auto-generated).
        selection (ForeignKey): A reference to the Selection to which this quote belongs.
        file (FileField): The uploaded PDF file for the quote.
        created_at (DateTimeField): The timestamp when the quote was created.
    """
    
    selection = models.ForeignKey(Selection, on_delete=models.CASCADE, related_name='quotes')
    file = models.FileField(upload_to='quotes/')  # PDF validation
    status = models.CharField(
        max_length=10,
        choices=QUOTE_STATUS_CHOICES,
        default=QUOTE_PENDING
    )

    def __str__(self):
        return f"Quote {self.id} for Selection {self.selection.id}"
