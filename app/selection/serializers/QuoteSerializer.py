"""
Module: Quote Serializer

This module defines the QuoteSerializer class, which serializes the Quote model for representation
and validation.

Classes:
    QuoteSerializer: Serializes the Quote model and enforces validation rules.

Attributes:
    id: The unique identifier for the quote.
    selection: The selection to which this quote belongs.
    file: The uploaded file for the quote.
    created_at: The timestamp when the quote was created.
"""

from rest_framework import serializers
from app.selection.models.Quote import Quote  

class QuoteSerializer(serializers.ModelSerializer):
    """
    Serializer for the Quote model.
    
    Attributes:
        id: The unique identifier for the quote.
        selection: The selection to which this quote belongs.
        file: The uploaded file for the quote.
        created_at: The timestamp when the quote was created.
    """
    
    class Meta:
        model = Quote
        fields = ['id', 'selection', 'file', 'created_at','status']

    def validate_file(self, value):
        """
        Ensure the uploaded file is a PDF.
        """
        if not value.name.endswith('.pdf'):
            raise serializers.ValidationError("The file must be a PDF.")
        return value

    def validate_selection(self, value):
        """
        Ensure that a quote can only be created for a selection with a phase number higher than 1.
        """
        phase = value.phase  
        if phase and phase.number <= 1:
            raise serializers.ValidationError("""A quote can only be created for a 
                                              selection with a phase number higher than 1.""")
        return value