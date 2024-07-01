from django.urls import path
from app.announcement.controllers import AnnouncementViewSet

announcement_urlpatterns = [
    path("announcement/create/", AnnouncementViewSet.as_view({'post': 'create_announcement'}), name="create-announcement"),
    path("announcement/update/<int:pk>/", AnnouncementViewSet.as_view({'put': 'update_announcement'}), name="update-announcement"),
    path("announcement/architect-specialities/", AnnouncementViewSet.as_view({'get': 'get_architect_specialities'}), name="architect-specialities"),
    path("announcement/architect-speciality-needs/<int:architect_speciality_id>/", AnnouncementViewSet.as_view({'get': 'get_architect_speciality_needs'}), name="architect-speciality-needs"),
    path("announcement/project-categories/", AnnouncementViewSet.as_view({'get': 'get_project_categories'}), name="project-categories"),
    path("announcement/property-types/<int:project_category_id>/", AnnouncementViewSet.as_view({'get': 'get_property_types'}), name="property-types"),
    path("announcement/work-types/", AnnouncementViewSet.as_view({'get': 'get_announcement_work_types'}), name="work-types"),
    path("announcement/renovation-pieces/", AnnouncementViewSet.as_view({'get': 'get_renovation_pieces'}), name="renovation-pieces"),
    path("announcement/cities/", AnnouncementViewSet.as_view({'get': 'get_cities'}), name="cities"),
    path("announcement/terrain-surfaces/", AnnouncementViewSet.as_view({'get': 'get_terrain_surfaces'}), name="terrain-surfaces"),
    path("announcement/work-surfaces/", AnnouncementViewSet.as_view({'get': 'get_work_surfaces'}), name="work-surfaces"),
    path("announcement/budgets/", AnnouncementViewSet.as_view({'get': 'get_budgets'}), name="budgets"),
    path("announcement/architectural-styles/", AnnouncementViewSet.as_view({'get': 'get_architectural_styles'}), name="architectural-styles"),
    path("announcement/project-extensions/", AnnouncementViewSet.as_view({'get': 'get_project_extensions'}), name="project-extensions"),
]
