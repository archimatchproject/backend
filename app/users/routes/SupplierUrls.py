from django.urls import path
from app.users.controllers import SupplierViewSet

supplier_urlpatterns = [
    path("supplier/signup/", SupplierViewSet.as_view({'post': 'supplier_signup'}), name="signup"),
    path("supplier/login/", SupplierViewSet.as_view({'post': 'supplier_login'}), name="login"),
    path("supplier/first-connection/", SupplierViewSet.as_view({'post': 'supplier_first_cnx'}), name="first-connection"),
    path("supplier/update-profile/", SupplierViewSet.as_view({'put': 'supplier_update_profile'}), name="update-profile"),
    path("supplier/update-bio/", SupplierViewSet.as_view({'put': 'supplier_update_bio'}), name="update-bio"),
    path("supplier/update-presentation-video/", SupplierViewSet.as_view({'put': 'supplier_update_presentation_video'}), name="update-presentation-video"),
    path("supplier/update-links/", SupplierViewSet.as_view({'put': 'supplier_update_links'}), name="update-links"),
    path("supplier/speciality-types/", SupplierViewSet.as_view({'get': 'get_speciality_types'}), name="speciality-types"),
    path("supplier/appearances/", SupplierViewSet.as_view({'get': 'get_appearances'}), name="appearances"),
]