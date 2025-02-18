"""
exposed URLS for offer app
viewset : OfferViewSet
"""


from django.urls import path
from app.officeOffer.controllers.OfferViewSet import OfferViewSet

offer_urlpatterns = [
    path(
        "create-offer/",
        OfferViewSet.as_view({"post": "create_offer"}),
        name="create-offer",
    ),
    path(
        "update-offer/<int:pk>/",
        OfferViewSet.as_view({"put": "update_offer"}),
        name="update-offer",
    ),
    path(
        "list-offers/",
        OfferViewSet.as_view({"get": "list_offers"}),
        name="list-offers",
    ),
    path(
        "offer-details/<int:pk>/",
        OfferViewSet.as_view({"get": "offer_details"}),
        name="offer-details",
    ),
    path(
        "contract-types/",
        OfferViewSet.as_view({"get": "get_contract_types"}),
        name="contract-types",
    ),
    path(
        "contract-durations/",
        OfferViewSet.as_view({"get": "get_contract_durations"}),
        name="contract-durations",
    ),
    path(
        "work-locations/",
        OfferViewSet.as_view({"get": "get_work_locations"}),
        name="work-locations",
    ),
    path(
        "salary-ranges/",
        OfferViewSet.as_view({"get": "get_salary_ranges"}),
        name="salary-ranges",
    ),
    path(
        "experience-levels/",
        OfferViewSet.as_view({"get": "get_experience_levels"}),
        name="experience-levels",
    ),
]
