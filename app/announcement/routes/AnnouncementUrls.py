"""
exposed URLS for announcement app
viewset : AnnouncementViewSet
"""

from django.urls import path

from app.announcement.controllers.AnnouncementViewSet import AnnouncementViewSet


announcement_urlpatterns = [
    path(
        "create-announcement/",
        AnnouncementViewSet.as_view({"post": "create_announcement"}),
        name="create-announcement",
    ),
    path(
        "update-announcement/<int:pk>/",
        AnnouncementViewSet.as_view({"put": "update_announcement"}),
        name="update-announcement",
    ),
    path(
        "update-announcement-images/<int:pk>/",
        AnnouncementViewSet.as_view({"put": "update_announcement_images"}),
        name="update-announcement",
    ),
    path(
        "architect-specialities/",
        AnnouncementViewSet.as_view({"get": "get_architect_specialities"}),
        name="architect-specialities",
    ),
    path(
        "architect-speciality-needs/<int:architect_speciality_id>/",
        AnnouncementViewSet.as_view({"get": "get_architect_speciality_needs"}),
        name="architect-speciality-needs",
    ),
    path(
        "project-categories/",
        AnnouncementViewSet.as_view({"get": "get_project_categories"}),
        name="project-categories",
    ),
    path(
        "property-types/<int:project_category_id>/",
        AnnouncementViewSet.as_view({"get": "get_property_types"}),
        name="property-types",
    ),
    path(
        "work-types/<int:property_type_id>",
        AnnouncementViewSet.as_view({"get": "get_announcement_work_types"}),
        name="work-types",
    ),
    path(
        "renovation-pieces/<int:property_type_id>",
        AnnouncementViewSet.as_view({"get": "get_renovation_pieces"}),
        name="renovation-pieces",
    ),
    path(
        "cities/",
        AnnouncementViewSet.as_view({"get": "get_cities"}),
        name="cities",
    ),
    path(
        "terrain-surfaces/",
        AnnouncementViewSet.as_view({"get": "get_terrain_surfaces"}),
        name="terrain-surfaces",
    ),
    path(
        "work-surfaces/",
        AnnouncementViewSet.as_view({"get": "get_work_surfaces"}),
        name="work-surfaces",
    ),
    path(
        "budgets/",
        AnnouncementViewSet.as_view({"get": "get_budgets"}),
        name="budgets",
    ),
    path(
        "architectural-styles/",
        AnnouncementViewSet.as_view({"get": "get_architectural_styles"}),
        name="architectural-styles",
    ),
    path(
        "project-extensions/<int:property_type_id>",
        AnnouncementViewSet.as_view({"get": "get_project_extensions"}),
        name="project-extensions",
    ),
]
