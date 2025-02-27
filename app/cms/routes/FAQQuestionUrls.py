"""
Exposed URLs for the cms app.

This module defines the URL patterns for the FAQQuestionViewSet,
providing separate paths for each CRUD operation.
"""

from django.urls import path

from app.cms.controllers.FAQQuestionViewSet import FAQQuestionViewSet


faq_question_urlpatterns = [
    path(
        "faq-question",
        FAQQuestionViewSet.as_view({"get": "list"}),
        name="faq-question-list",
    ),
    path(
        "faq-question/create/",
        FAQQuestionViewSet.as_view({"post": "create"}),
        name="faq-question-create",
    ),
    path(
        "faq-question/<int:pk>",
        FAQQuestionViewSet.as_view({"get": "retrieve"}),
        name="faq-question-detail",
    ),
    path(
        "faq-question/update/<int:pk>/",
        FAQQuestionViewSet.as_view({"put": "update"}),
        name="faq-question-update",
    ),
    path(
        "faq-question/delete/<int:pk>/",
        FAQQuestionViewSet.as_view({"delete": "destroy"}),
        name="faq-question-delete",
    ),
]
