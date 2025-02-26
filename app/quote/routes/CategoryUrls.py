"""
Exposed URLs for category app
viewset : CategoryViewSet
"""

from django.urls import path

from app.quote.controllers.CategoryViewSet import CategoryViewSet


category_urlpatterns = [
    path(
        "category/get-all",
        CategoryViewSet.as_view({"get": "get_all_categories"}),
        name="get-all",
    ),
    path(
        "category/create",
        CategoryViewSet.as_view({"post": "create_category"}),
        name="create",
    ),
    path(
        "category/delete/<int:pk>/",
        CategoryViewSet.as_view({"delete": "delete_category"}),
        name="delete",
    ),
]
