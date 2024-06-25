"""
This module configures the translation options for the Block model using the modeltranslation library.

It registers the Block model for translation and specifies which fields should be translated.
"""

from modeltranslation.translator import TranslationOptions, register

from app.cms.models import Block


@register(Block)
class BlockTranslationOptions(TranslationOptions):
    """
    Translation options for the Block model.

    This class defines which fields of the Block model will have translations.
    """

    fields = ("content",)
