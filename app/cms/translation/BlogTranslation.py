"""
This module configures the translation options for the Blog model using the modeltranslation library.

It registers the Blog model for translation and specifies which fields should be translated.
"""

from modeltranslation.translator import TranslationOptions, register

from app.cms.models import Blog


@register(Blog)
class BlogTranslationOptions(TranslationOptions):
    """
    Translation options for the Blog model.

    This class defines which fields of the Blog model will have translations.
    """

    fields = ("title",)
