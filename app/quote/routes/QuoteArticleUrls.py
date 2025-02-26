"""
exposed URLS for quote app
viewset : QuoteArticleViewSet
"""

from django.urls import path

from app.quote.controllers.QuoteArticleViewSet import QuoteArticleViewSet


quoteArticle_urlpatterns = [
    path(
        "article/get-all",
        QuoteArticleViewSet.as_view({"get": "get_all_quoteArticles"}),
        name="get-all",
    ),
    path(
        "article/create",
        QuoteArticleViewSet.as_view({"post": "create_quoteArticle"}),
        name="create",
    ),
    path(
        "article/update/<int:pk>/",
        QuoteArticleViewSet.as_view({"post": "update_quoteArticle"}),
        name="update",
    ),
    path(
        "article/delete/<int:pk>/",
        QuoteArticleViewSet.as_view({"delete": "delete_quoteArticle"}),
        name="delete",
    ),
]
