"""
Module: announcement Service

This module defines the AnnouncementService class that handles announcement-related operations .

Classes:
    AnnouncementService: Service class for announcement-related operations.

"""

from django.contrib.auth.models import AnonymousUser
from django.db import transaction
from django.utils.translation import get_language_from_request

from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from app.announcement import ACCEPTED
from app.announcement import BUDGETS
from app.announcement import CITIES
from app.announcement import EXTERIOR_WORKTYPES
from app.announcement import NEW_CONSTRUCTION_WORKTYPES
from app.announcement import NOT_ELIMINATE_STEP_PROPERTIES_STEP6
from app.announcement import NOT_ELIMINATE_STEP_PROPERTIES_STEP10
from app.announcement import PROPERTIES_NO_EXTERIOR
from app.announcement import REFUSED
from app.announcement import RENOVATION_WORKTYPES
from app.announcement import TERRAIN_SURFACES
from app.announcement import WORK_SURFACES
from app.announcement.models.Announcement import Announcement
from app.announcement.models.AnnouncementPieceRenovate import AnnouncementPieceRenovate
from app.announcement.models.Need import Need
from app.announcement.models.PieceRenovate import PieceRenovate
from app.announcement.models.ProjectExtension import ProjectExtension
from app.announcement.models.ProjectImage import ProjectImage
from app.announcement.serializers.AnnouncementSerializer import AnnouncementOutputSerializer
from app.announcement.serializers.AnnouncementSerializer import AnnouncementPOSTSerializer
from app.announcement.serializers.AnnouncementSerializer import AnnouncementPUTSerializer
from app.announcement.serializers.ArchitectSpecialitySerializer import ArchitectSpecialitySerializer
from app.announcement.serializers.ArchitecturalStyleSerializer import ArchitecturalStyleSerializer
from app.announcement.serializers.NeedSerializer import NeedSerializer
from app.announcement.serializers.PieceRenovateSerializer import PieceRenovateSerializer
from app.announcement.serializers.ProjectCategorySerializer import ProjectCategorySerializer
from app.announcement.serializers.ProjectExtensionSerializer import ProjectExtensionSerializer
from app.announcement.serializers.PropertyTypeSerializer import PropertyTypeSerializer
from app.announcement.serializers.WorkTypeSerializer import WorkTypeSerializer
from app.core.models.ArchitectSpeciality import ArchitectSpeciality
from app.core.models.ArchitecturalStyle import ArchitecturalStyle
from app.core.models.Note import Note
from app.core.models.ProjectCategory import ProjectCategory
from app.core.models.PropertyType import PropertyType
from app.core.models.WorkType import WorkType
from app.core.pagination import CustomPagination
from app.core.serializers.NoteSerializer import NoteSerializer
from app.email_templates.signals import api_success_signal
from app.users import USER_TYPE_CHOICES
from app.users.models import Client
from app.users.models.ArchimatchUser import ArchimatchUser
from app.users.serializers.ArchimatchUserSerializer import ArchimatchUserSerializer
from app.users.utils import generate_password_reset_token
from project_core.django import base as settings


class AnnouncementService:
    """
    Service class for handling announcement-related operations .

    """

    pagination_class = CustomPagination

    @classmethod
    def create_announcement(cls, request):
        """
        Creating new announcement
        """
        data = request.data
        user = request.user
        serializer = AnnouncementPOSTSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            needs_data = validated_data.pop("needs")
            pieces_renovate_data = validated_data.pop("pieces_renovate", [])
            project_extensions_data = validated_data.pop("project_extensions")
            project_images_data = validated_data.pop("project_images", [])
            client_data = validated_data.pop("client", None)

            with transaction.atomic():
                if client_data:
                    user_data = client_data.pop("user")
                    user_data["username"] = user_data["email"]
                    user_data["user_type"] = USER_TYPE_CHOICES[1][0]
                    user_serializer = ArchimatchUserSerializer(data=user_data)
                    user_serializer.is_valid(raise_exception=True)
                    user_instance = ArchimatchUser.objects.create(**user_data)
                    client_instance = Client.objects.create(
                        user=user_instance,
                        **client_data,
                    )
                    token = generate_password_reset_token(client_instance.user.id, expires_in=3600)
                    email_images = settings.CLIENT_FIRST_CONNECTION_IMAGES
                    language_code = get_language_from_request(request)
                    url = f"""{settings.BASE_FRONTEND_URL}/{language_code}"""
                    reset_link = f"""{url}/client/first-login/{token}"""
                    context = {
                        "first_name": client_instance.user.first_name,
                        "last_name": client_instance.user.last_name,
                        "email": client_instance.user.email,
                        "reset_link": reset_link,
                    }
                    signal_data = {
                        "template_name": "client_first_connection.html",
                        "context": context,
                        "to_email": client_instance.user.email,
                        "subject": "Client Account Creation",
                        "images": email_images,
                    }
                    api_success_signal.send(sender=cls, data=signal_data)
                else:
                    if isinstance(user, AnonymousUser):
                        raise serializers.ValidationError(
                            detail="You must be logged in to create an announcement. \
                            Please provide a valid authentication token."
                        )
                    client_instance = Client.objects.get(user=user)

                announcement = Announcement.objects.create(client=client_instance, **validated_data)
                announcement.needs.set(needs_data)

                for piece_data in pieces_renovate_data:
                    for piece_renovate_id, number in piece_data.items():
                        piece_renovate = PieceRenovate.objects.get(pk=piece_renovate_id)
                        AnnouncementPieceRenovate.objects.create(
                            announcement=announcement, piece_renovate=piece_renovate, number=number
                        )

                announcement.project_extensions.set(project_extensions_data)

                for image in project_images_data:
                    ProjectImage.objects.create(announcement=announcement, image=image)

            return Response(
                {
                    "message": "Announcement created successfully",
                    "data": AnnouncementOutputSerializer(announcement).data,
                },
                status=status.HTTP_201_CREATED,
            )
        except serializers.ValidationError as e:
            raise e
        except Client.DoesNotExist:
            raise NotFound(detail="Client not found")
        except Exception as e:
            raise APIException(detail=f"Error creating announcement ${str(e)}")

    @classmethod
    def update_announcement(cls, instance, data):
        """
        Updating existing announcement
        """
        print(data)
        serializer = AnnouncementPUTSerializer(instance, data=data, partial=True)
        if not serializer.is_valid(raise_exception=True):
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        validated_data = serializer.validated_data

        try:
            needs_data = validated_data.pop("needs", [])
            pieces_renovate_data = validated_data.pop("pieces_renovate", [])
            project_extensions_data = validated_data.pop("project_extensions", [])
            project_images_data = validated_data.pop("project_images", [])

            # Update needs if data is not empty
            if needs_data:
                instance.needs.set(needs_data)

            # Update pieces_renovate if data is not empty
            if pieces_renovate_data:
                print("aaaaaaaaaaaaaaa", pieces_renovate_data)
                AnnouncementPieceRenovate.objects.filter(announcement=instance).delete()
                for piece_data in pieces_renovate_data:
                    for piece_renovate_id, number in piece_data.items():
                        piece_renovate = PieceRenovate.objects.get(pk=piece_renovate_id)
                        AnnouncementPieceRenovate.objects.create(
                            announcement=instance,
                            piece_renovate=piece_renovate,
                            number=number,
                        )

            # Update project_extensions if data is not empty
            if project_extensions_data:
                instance.project_extensions.set(project_extensions_data)

            # Update project_images if data is not empty
            if project_images_data:
                ProjectImage.objects.filter(announcement=instance).delete()
                for image in project_images_data:
                    ProjectImage.objects.create(
                        announcement=instance,
                        image=image,
                    )

            # Update other attributes if any
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            return Response(
                {
                    "message": "Announcement updated successfully",
                    "data": AnnouncementOutputSerializer(instance).data,
                },
                status=status.HTTP_200_OK,
            )
        except serializers.ValidationError as e:
            raise e
        except Exception:
            raise APIException(detail="Error updating announcement")

    @classmethod
    def update_announcement_images(cls, instance, request):
        """
        Updating existing announcement images
        """
        try:
            project_images_files = request.data.getlist("projectImages")
            with transaction.atomic():
                # Clear existing images
                instance.project_images.all().delete()
                # Add new images
                for image in project_images_files:
                    ProjectImage.objects.create(
                        announcement=instance,
                        image=image,
                    )

            return Response(
                {
                    "message": "Announcement images updated successfully",
                    "data": AnnouncementOutputSerializer(instance).data,
                },
                status=status.HTTP_200_OK,
            )
        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error updating announcement images: {str(e)}")

    @classmethod
    def get_architect_specialities(cls):
        """
        Retrieves all architect specialities.

        Returns:
            Response: Response containing list of architect specialities.
        """
        try:
            architect_specialities = ArchitectSpeciality.objects.all()
            serializer = ArchitectSpecialitySerializer(
                architect_specialities,
                many=True,
            )

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        except Exception:
            raise APIException("Error retrieving architect specialities")

    @classmethod
    def get_architect_speciality_needs(cls, architect_speciality_id):
        """
        Retrieves needs based on architect speciality.

        Args:
            architect_speciality_id (int): ID of the architect speciality.

        Returns:
            Response: Response containing list of needs related to the architect speciality.
        """
        try:
            if not ArchitectSpeciality.objects.filter(id=architect_speciality_id).exists():
                raise NotFound(detail="No architect speciality found with the given ID")

            needs = Need.objects.filter(architect_speciality_id=architect_speciality_id)
            serializer = NeedSerializer(needs, many=True)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        except NotFound as e:
            raise e
        except Exception:
            raise APIException(detail="Error retrieving architect speciality needs")

    @classmethod
    def get_project_categories(cls):
        """
        Retrieves all project categories.

        Returns:
        Response: Response containing list of project categories.
        """
        try:
            project_categories = ProjectCategory.objects.all()
            serializer = ProjectCategorySerializer(project_categories, many=True)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        except Exception:
            raise APIException("Error retrieving project categories")

    @classmethod
    def get_property_types(cls, project_category_id):
        """
        Retrieves property types based on project category.

        Args:
            project_category_id (int): ID of the project category.

        Returns:
            Response: Response containing list of property types related to the project category.
        """
        try:
            if not ProjectCategory.objects.filter(id=project_category_id).exists():
                raise NotFound(detail="No project category found with the given ID")

            property_types = PropertyType.objects.filter(project_category_id=project_category_id)
            serializer = PropertyTypeSerializer(property_types, many=True)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        except NotFound as e:
            raise e
        except Exception:
            raise APIException(detail="Error retrieving property types")

    @classmethod
    def get_announcement_work_types(cls, property_type_id):
        """
        Retrieves announcement work types optionally filtered by property type.

        Args:
            property_type_id (int, optional): ID of the property type to filter work types.
            Defaults to None.

        Returns:
            Response: Response containing list of announcement work types.
        """
        try:

            if not PropertyType.objects.filter(id=property_type_id).exists():
                raise NotFound(detail="No property type found with the given ID")
            work_types = WorkType.objects.all()
            if int(property_type_id) in PROPERTIES_NO_EXTERIOR:
                work_types = work_types.exclude(id__in=EXTERIOR_WORKTYPES)
            serializer = WorkTypeSerializer(work_types, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except NotFound as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error retrieving announcement work types, ${str(e)}")

    @classmethod
    def get_renovation_pieces(cls, property_type_id, work_type_id):
        """
        Retrieves all renovation pieces.

        Returns:
            Response: Response containing list of renovation pieces.
        """
        try:
            if not PropertyType.objects.filter(id=property_type_id).exists():
                raise NotFound(detail="No property type found with the given ID")
            if not WorkType.objects.filter(id=work_type_id).exists():
                raise NotFound(detail="No work type found with the given ID")

            renovation_pieces = PieceRenovate.objects.filter(property_type_id=property_type_id)
            serializer = PieceRenovateSerializer(renovation_pieces, many=True)
            return Response(
                data={
                    "data": serializer.data,
                    "new_construction": int(work_type_id) not in RENOVATION_WORKTYPES,
                    "eliminate_step": int(property_type_id)
                    not in NOT_ELIMINATE_STEP_PROPERTIES_STEP6,
                },
                status=status.HTTP_200_OK,
            )

        except NotFound as e:
            raise e
        except Exception:
            raise APIException("Error retrieving renovation pieces")

    @classmethod
    def get_cities(cls):
        """
        Retrieves predefined cities choices.

        Returns:
            Response: Response containing list of cities.
        """
        try:
            cities = [
                {
                    "value": city[0],
                    "display_name": city[1],
                }
                for city in CITIES
            ]
            return Response(cities, status=status.HTTP_200_OK)
        except Exception:
            raise APIException("Error retrieving cities")

    @classmethod
    def get_terrain_surfaces(cls):
        """
        Retrieves predefined terrain surfaces choices.

        Returns:
            Response: Response containing list of terrain surfaces.
        """
        try:
            terrain_surfaces = [
                {
                    "value": surface[0],
                    "display_name": surface[1],
                }
                for surface in TERRAIN_SURFACES
            ]
            return Response(
                terrain_surfaces,
                status=status.HTTP_200_OK,
            )
        except Exception:
            raise APIException("Error retrieving terrain surfaces")

    @classmethod
    def get_work_surfaces(cls):
        """
        Retrieves predefined work surfaces choices.

        Returns:
            Response: Response containing list of work surfaces.
        """
        try:
            work_surfaces = [
                {
                    "value": surface[0],
                    "display_name": surface[1],
                }
                for surface in WORK_SURFACES
            ]
            return Response(
                work_surfaces,
                status=status.HTTP_200_OK,
            )
        except Exception:
            raise APIException("Error retrieving work surfaces")

    @classmethod
    def get_budgets(cls):
        """
        Retrieves predefined budgets choices.

        Returns:
            Response: Response containing list of budgets.
        """
        try:
            budgets = [
                {
                    "value": budget[0],
                    "display_name": budget[1],
                }
                for budget in BUDGETS
            ]
            return Response(budgets, status=status.HTTP_200_OK)
        except Exception:
            raise APIException("Error retrieving budgets")

    @classmethod
    def get_architectural_styles(cls, property_type_id):
        """
        Retrieves all architectural styles.

        Returns:
            Response: Response containing list of architectural styles.
        """
        try:
            architectural_styles = ArchitecturalStyle.objects.all()
            serializer = ArchitecturalStyleSerializer(
                architectural_styles,
                many=True,
            )
            return Response(
                data={
                    "data": serializer.data,
                    "eliminate_step": int(property_type_id)
                    not in NOT_ELIMINATE_STEP_PROPERTIES_STEP6,
                },
                status=status.HTTP_200_OK,
            )
        except Exception:
            return APIException("Error retrieving architectural styles")

    @classmethod
    def get_project_extensions(cls, property_type_id, work_type_id):
        """
        Retrieves all project extensions.

        Returns:
            Response: Response containing list of project extensions.
        """
        try:
            if not PropertyType.objects.filter(id=property_type_id).exists():
                raise NotFound(detail="No property type found with the given ID")
            if not WorkType.objects.filter(id=work_type_id).exists():
                raise NotFound(detail="No work type found with the given ID")
            project_extensions = ProjectExtension.objects.filter(property_type_id=property_type_id)
            serializer = ProjectExtensionSerializer(project_extensions, many=True)
            return Response(
                data={
                    "data": serializer.data,
                    "eliminate_step": (
                        int(property_type_id) not in NOT_ELIMINATE_STEP_PROPERTIES_STEP10
                    )
                    and int(work_type_id) in NEW_CONSTRUCTION_WORKTYPES,
                },
                status=status.HTTP_200_OK,
            )
        except NotFound as e:
            raise e
        except Exception:
            raise APIException("Error retrieving renovation pieces")

    @classmethod
    def add_note_to_announcement(cls, announcement_id, data):
        """
        Handles adding a note to an ArchitectRequest.

        Args:
            announcement_id (int): The ID of the ArchitectRequest to which the note will be added.
            data (dict): The validated data for creating a new Note.

        Returns:
            Response: The response object containing the result of the operation.
        """
        try:
            announcement = Announcement.objects.get(pk=announcement_id)

            serializer = NoteSerializer(data=data)
            serializer.is_valid(raise_exception=True)

            note = Note.objects.create(
                message=serializer.validated_data["message"],
                content_object=announcement,
            )

            return Response(NoteSerializer(note).data, status=status.HTTP_201_CREATED)
        except Announcement.DoesNotExist:
            raise NotFound(detail="No announcement found with the given ID")
        except Exception as e:
            raise APIException(detail=f"Error adding not to announcement ${e}")

    @classmethod
    def get_announcements(cls, request):
        """
        Handle GET request and return paginated Announcement objects.

        This method retrieves all Announcement objects from the database, applies
        pagination based on the parameters in the request, and returns the paginated
        results. If the pagination is not applied correctly, it returns a 400 Bad Request response.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Response: A paginated response containing Announcement objects or an error message.
        """
        queryset = Announcement.objects.all()
        paginator = cls.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = AnnouncementOutputSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = AnnouncementOutputSerializer(queryset, many=True)
        return Response({"message": "error retrieving data"}, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def accept_announcement(cls, pk):
        """
        Custom action to accept an Announcement.

        Args:
            request (Request): The request object containing the input data.
            pk (str): The primary key of the Announcement to be accepted.

        Returns:
            Response: The response object containing the result of the acceptance operation.
        """
        try:
            announcement = Announcement.objects.get(pk=pk)
            announcement.status = ACCEPTED
            announcement.save()
            return Response({"message": "announcement Accepted"}, status=status.HTTP_200_OK)
        except Announcement.DoesNotExist:
            raise NotFound(detail="Announcement not found")
        except APIException as e:
            raise NotFound(detail=str(e))
        except Exception:
            raise APIException(detail="Error accepting the announcement")

    @classmethod
    def refuse_announcement(cls, pk):
        """
        Custom action to refuse an Announcement.

        Args:
            request (Request): The request object containing the input data.
            pk (str): The primary key of the Announcement to be refused.

        Returns:
            Response: The response object containing the result of the refusal operation.
        """
        try:
            announcement = Announcement.objects.get(pk=pk)
            announcement.status = REFUSED
            announcement.save()
            return Response({"message": "announcement refused"}, status=status.HTTP_200_OK)
        except Announcement.DoesNotExist:
            raise NotFound(detail="Announcement not found")
        except APIException as e:
            raise NotFound(detail=str(e))
        except Exception:
            raise APIException(detail="Error accepting the announcement")

    @classmethod
    def get_announcement_details(cls, pk):
        """
        Custom action to refuse an Announcement.

        Args:
            request (Request): The request object containing the input data.
            pk (str): The primary key of the Announcement to be refused.

        Returns:
            Response: The response object containing the result of the refusal operation.
        """
        try:
            announcement = Announcement.objects.get(pk=pk)

            serializer = AnnouncementOutputSerializer(announcement, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Announcement.DoesNotExist:
            raise NotFound(detail="Announcement not found")
        except APIException as e:
            raise e
        except Exception:
            raise APIException(detail="Error retrieving the announcement")
