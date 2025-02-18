from app.officeOffer import CONTRACT_TYPES
from app.officeOffer import CONTRACT_DURATIONS
from app.officeOffer import WORK_LOCATIONS
from app.officeOffer import SALARY_RANGES
from app.officeOffer import EXPERIENCE_CHOICES
from django.db import transaction

from app.officeOffer.models import Offer

from app.officeOffer.serializers import OfferPOSTSerializer, OfferOutputSerializer
from django.contrib.auth.models import AnonymousUser
from app.users.models.Office import Office
from app.officeOffer.serializers.OfferSerializer import OfferPUTSerializer
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from app.core.pagination import CustomPagination


class OfferService:
    """
    Service class for handling offer-related operations.
    """

    pagination_class = CustomPagination

    @classmethod
    def create_offer(cls, request):
        """
        Create a new job offer.
        """
        data = request.data
        user = request.user

        serializer = OfferPOSTSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        technical_skills_data = validated_data.pop("technical_skills", [])
        software_skills_data = validated_data.pop("software_skills", [])

        if isinstance(user, AnonymousUser):
            raise serializers.ValidationError(
                        detail="You must be a valid office to create an offer"
                    )
        office_instance = Office.objects.get(user=user)
        
        with transaction.atomic():
            offer = Offer.objects.create(office=office_instance, **validated_data)
            offer.technical_skills.set(technical_skills_data)
            offer.software_skills.set(software_skills_data)

        return True, OfferOutputSerializer(offer).data, "Offer created successfully"
    
    @classmethod
    def update_offer(cls, instance, data):
        """
        Update an existing job offer.
        """
        serializer = OfferPUTSerializer(instance, data=data, partial=True)
        if not serializer.is_valid(raise_exception=True):
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        validated_data = serializer.validated_data

        technical_skills_data = validated_data.pop("technical_skills", [])
        software_skills_data = validated_data.pop("software_skills", [])

        with transaction.atomic():
            if technical_skills_data:
                instance.technical_skills.set(technical_skills_data)

            if software_skills_data:
                instance.software_skills.set(software_skills_data)

            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            instance.save()

        return True, OfferOutputSerializer(instance).data, "Offer updated successfully"
    
    @classmethod
    def get_offers(cls, request):
        """
        Retrieve and return paginated job offers.

        This method retrieves all Offer objects, applies filters based on query parameters,
        paginates the results, and returns them in a paginated response.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Response: A paginated response containing Offer objects or an error message.
        """
        queryset = Offer.objects.all().order_by("created_at")
        paginator = cls.pagination_class()

        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = OfferOutputSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = OfferOutputSerializer(queryset, many=True)
        return Response({"message": "Error retrieving data"}, status=status.HTTP_400_BAD_REQUEST)
    
    @classmethod
    def get_offer_details(cls, request, pk):
        """
        Retrieve details of a specific job offer.

        Args:
            request (Request): The request object containing the input data.
            pk (str): The primary key of the Offer to be retrieved.

        Returns:
            tuple: (bool, dict) containing success status and offer details.
        """
        offer = Offer.objects.get(pk=pk)
        
        serializer = OfferOutputSerializer(offer, many=False, context={'request': request})
        return True, serializer.data
    
    @classmethod
    def get_contract_types(cls):
        """
        Retrieves predefined contract types.

        Returns:
            tuple: (bool, list) containing success status and contract types.
        """
        contract_types = [{"value": ct[0], "display_name": ct[1]} for ct in CONTRACT_TYPES]
        return True, contract_types

    @classmethod
    def get_contract_durations(cls):
        """
        Retrieves predefined contract durations.

        Returns:
            tuple: (bool, list) containing success status and contract durations.
        """
        contract_durations = [{"value": cd[0], "display_name": cd[1]} for cd in CONTRACT_DURATIONS]
        return True, contract_durations

    @classmethod
    def get_work_locations(cls):
        """
        Retrieves predefined work locations.

        Returns:
            tuple: (bool, list) containing success status and work locations.
        """
        work_locations = [{"value": wl[0], "display_name": wl[1]} for wl in WORK_LOCATIONS]
        return True, work_locations

    @classmethod
    def get_salary_ranges(cls):
        """
        Retrieves predefined salary ranges.

        Returns:
            tuple: (bool, list) containing success status and salary ranges.
        """
        salary_ranges = [{"value": sr[0], "display_name": sr[1]} for sr in SALARY_RANGES]
        return True, salary_ranges

    @classmethod
    def get_experience_levels(cls):
        """
        Retrieves predefined experience levels.

        Returns:
            tuple: (bool, list) containing success status and experience levels.
        """
        experience_levels = [
            {"value": exp[0], "display_name": exp[1]} for exp in EXPERIENCE_CHOICES]
        return True, experience_levels
