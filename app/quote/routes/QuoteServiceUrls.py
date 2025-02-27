"""
Exposed URLs for quote app
viewset : QuoteServiceViewSet
"""

from django.urls import path

from app.quote.controllers.QuoteServiceViewSet import QuoteServiceViewSet


quote_service_urlpatterns = [
    path(
        "service/get-all",
        QuoteServiceViewSet.as_view({"get": "get_all_quote_services"}),
        name="get-all",
    ),
    path(
        "service/create",
        QuoteServiceViewSet.as_view({"post": "create_quote_service"}),
        name="create",
    ),
    path(
        "service/update/<int:pk>/",
        QuoteServiceViewSet.as_view({"put": "update_quote_service"}),
        name="update",
    ),
    path(
        "service/delete/<int:pk>/",
        QuoteServiceViewSet.as_view({"delete": "delete_quote_service"}),
        name="delete",
    ),
]
