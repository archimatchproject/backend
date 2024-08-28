"""
Service module for the Collection model.

This module defines the service for handling the business logic and exceptions
related to Collection creation and management.

Classes:
    CollectionService: Service class for Collection operations.
"""

from django.db import transaction

from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from app.catalogue.models.Collection import Collection
from app.catalogue.models.Product import Product
from app.catalogue.serializers.CollectionSerializer import CollectionSerializer
from app.core.pagination import CustomPagination
from app.users.models.Supplier import Supplier


class CollectionService:
    """
    Service class for handling Collection operations.

    Handles business logic and exception handling for Collection creation and management.

    Methods:
        create_collection(request, data): Handles validation and creation of a new Collection.
    """
    
    pagination_class = CustomPagination

    @classmethod
    def create_collection(cls, request):
        """
        Handles validation and creation of a new Collection.

        Args:
            request (Request): The request object containing the authenticated user.

        Returns:
            Response: The response object containing the result of the operation.
        """
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        user = request.user
        try:
            supplier = Supplier.objects.get(user=user)
            with transaction.atomic():
                # Create Collection instance
                collection = Collection.objects.create(supplier=supplier, **validated_data)
                supplier.speciality_type.add(validated_data.get("category"))
                return Response(
                    CollectionSerializer(collection).data,
                    status=status.HTTP_201_CREATED,
                )
        except Supplier.DoesNotExist:
            raise NotFound(detail="Authenticated user is not a supplier.")
        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error creating collection: {str(e)}")

    @classmethod
    def update_product_order(cls, request, pk):
        """
        Handles updating the order of products within a collection.

        Args:
            request (Request): The request object containing the authenticated user.
            pk (int): The primary key of the collection.

        Returns:
            Response: The response object containing the result of the operation.
        """
        product_ids = request.data.get("product_ids")

        try:
            if not product_ids:
                raise serializers.ValidationError(detail="Product IDs are required.")
            collection = Collection.objects.get(pk=pk)
            if collection.supplier.user != request.user:
                raise serializers.ValidationError(
                    detail="You do not have permission to modify this collection."
                )

            with transaction.atomic():
                for index, product_id in enumerate(product_ids):
                    Product.objects.filter(id=product_id, collection=collection).update(order=index)

            return Response("Product order updated successfully.", status=status.HTTP_200_OK)
        except Collection.DoesNotExist:
            raise NotFound(detail="Collection not found.")
        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error updating product order: {str(e)}")

    @classmethod
    def update_display_status(cls, request, pk):
        """
        Handles updating the display status of a collection.

        Args:
            request (Request): The request object containing the authenticated user.
            pk (int): The primary key of the collection.

        Returns:
            Response: The response object containing the result of the operation.
        """
        display_status = request.data.get("display")
        try:
            if display_status is None:
                raise serializers.ValidationError(detail="Display status is required.")
            collection = Collection.objects.get(pk=pk)
            if collection.supplier.user != request.user:
                raise serializers.ValidationError(
                    detail="You do not have permission to modify this collection."
                )

            collection.display = display_status
            collection.save()

            return Response(
                "Collection display status updated successfully.", status=status.HTTP_200_OK
            )
        except Collection.DoesNotExist:
            raise NotFound(detail="Collection not found.")
        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error updating collection display status: {str(e)}")

    @classmethod
    def update_visibility(cls, request, pk):
        """
        Handles updating the display status of a collection.

        Args:
            request (Request): The request object containing the authenticated user.
            pk (int): The primary key of the collection.

        Returns:
            Response: The response object containing the result of the operation.
        """
        visibility = request.data.get("visibility")
        try:
            if visibility is None:
                raise serializers.ValidationError(detail="visibility is required.")
            collection = Collection.objects.get(pk=pk)
            if collection.supplier.user != request.user:
                raise serializers.ValidationError(
                    detail="You do not have permission to modify this collection."
                )

            collection.visibility = visibility
            collection.save()

            return Response(
                "Collection visibility updated successfully.", status=status.HTTP_200_OK
            )
        except Collection.DoesNotExist:
            raise NotFound(detail="Collection not found.")
        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error updating visibility status: {str(e)}")
        
    
    @classmethod
    def get_collections(cls, request):
        """
        Handle GET request and return paginated collection objects.
        This method retrieves all collection objects from the database, applies
        pagination based on the parameters in the request, and returns the paginated
        results. If the pagination parameters are not provided correctly or if an
        error occurs during serialization or database access, it returns a 400 Bad
        Request response with an appropriate error message.
        Args:
            request (HttpRequest): The incoming HTTP request object containing
                pagination parameters like page number, page size, etc.
        Returns:
            Response: A paginated response containing serialized collection objects
                or a 400 Bad Request response with an error message.
        """

        queryset = Collection.objects.filter(supplier__user=request.user)
        # Instantiate the paginator
        paginator = cls.pagination_class()

        # Apply pagination to the filtered queryset
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            print(page)
            serializer = CollectionSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @classmethod
    def create_saved_collections(cls, request):
        """
        Handles validation and creation of multiple Collections.

        Args:
            request (Request): The request object containing the authenticated user.

        Returns:
            Response: The response object containing the result of the operation.
        """
        user = request.user

        # Ensure the authenticated user is a supplier
        try:
            supplier = Supplier.objects.get(user=user)
        except Supplier.DoesNotExist:
            raise NotFound(detail="Authenticated user is not a supplier.")

        collections_data = request.data.get('collections', [])
        if not isinstance(collections_data, list):
            raise serializers.ValidationError({"collections": "This field must be a list of collections."})

        created_collections = []

        try:
            with transaction.atomic():
                for collection_data in collections_data:
                    serializer = CollectionSerializer(data=collection_data)
                    serializer.is_valid(raise_exception=True)
                    validated_data = serializer.validated_data
                    
                    # Create Collection instance
                    collection = Collection.objects.create(supplier=supplier, **validated_data)
                    supplier.speciality_type.add(validated_data.get("category"))
                    created_collections.append(CollectionSerializer(collection).data)

            return Response(
                created_collections,
                status=status.HTTP_201_CREATED,
            )
        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error creating collections: {str(e)}")