"""
Service module for the Product model.

This module defines the service for handling the business logic and exceptions
related to Product creation and management.

Classes:
    ProductService: Service class for Product operations.
"""

from django.db import transaction

from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from app.catalogue.models.Product import Product
from app.catalogue.models.ProductImage import ProductImage
from app.catalogue.serializers.ProductSerializer import ProductSerializer
from app.core.pagination import CustomPagination


class ProductService:
    """
    Service class for handling Product operations.

    Handles business logic and exception handling for Product creation and
      management.

    Methods:
        create_product(request, data): Handles validation and creation of a
        new Product.
        update_product(instance, request, data): Handles validation and updating
        of an existing Product.
    """
    pagination_class = CustomPagination
    
    @classmethod
    def create_product(cls, request):
        """
        Handles validation and creation of a new Product.

        Args:
            request (Request): The request object containing the authenticated user.
            data (dict): The validated data for creating a Product instance.

        Returns:
            Response: The response object containing the result of the operation.
        """
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        images_data = request.FILES.getlist("product_images")

        try:
            with transaction.atomic():
                # Create Product instance
                product = Product.objects.create(**validated_data)

                for image_data in images_data:
                    ProductImage.objects.create(product=product, image=image_data)

                return Response(
                    ProductSerializer(product).data,
                    status=status.HTTP_201_CREATED,
                )
        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error creating product: {str(e)}")

    @classmethod
    def update_product(cls, instance, request):
        """
        Handles validation and updating of an existing Product.

        Args:
            instance (Product): The existing Product instance.
            request (Request): The request object containing the authenticated user.

        Returns:
            Response: The response object containing the result of the operation.
        """
        serializer = ProductSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        images_data = request.FILES.getlist("product_images")

        try:
            with transaction.atomic():
                # Update Product instance
                fields = ["name", "price", "collection", "description","visibility"]
                for field in fields:
                    setattr(instance, field, validated_data.get(field, getattr(instance, field)))

                instance.save()

                if images_data:
                    with transaction.atomic():
                        instance.product_images.all().delete()
                        new_images = [
                            ProductImage(product=instance, image=image_data)
                            for image_data in images_data
                        ]
                        ProductImage.objects.bulk_create(new_images)

                return Response(
                    ProductSerializer(instance).data,
                    status=status.HTTP_200_OK,
                )
        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error updating product: {str(e)}")

    @classmethod
    def update_display_status(cls, request, pk):
        """
        Handles updating the display status of a product.

        Args:
            request (Request): The request object containing the authenticated user.
            pk (int): The primary key of the product.

        Returns:
            Response: The response object containing the result of the operation.
        """
        display_status = request.data.get("display")
        try:
            if display_status is None:
                raise serializers.ValidationError(detail="Display status is required.")
            product = Product.objects.get(pk=pk)
            if product.collection.supplier.user != request.user:
                raise serializers.ValidationError(
                    detail="You do not have permission to modify this product."
                )

            product.display = display_status
            product.save()

            return Response(
                "Product display status updated successfully.", status=status.HTTP_200_OK
            )
        except Product.DoesNotExist:
            raise NotFound(detail="Product not found.")
        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error updating product display status: {str(e)}")

    @classmethod
    def update_visibility(cls, request, pk):
        """
        Handles updating the visibility of a product.

        Args:
            request (Request): The request object containing the authenticated user.
            pk (int): The primary key of the product.

        Returns:
            Response: The response object containing the result of the operation.
        """
        visibility = request.data.get("visibility")
        try:
            if visibility is None:
                raise serializers.ValidationError(detail="visibility is required.")
            product = Product.objects.get(pk=pk)
            if product.collection.supplier.user != request.user:
                raise serializers.ValidationError(
                    detail="You do not have permission to modify this product."
                )

            product.visibility = visibility
            product.save()

            return Response(
                "visibility updated successfully.", status=status.HTTP_200_OK
            )
        except Product.DoesNotExist:
            raise NotFound(detail="Product not found.")
        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error updating product visibility: {str(e)}")


    @classmethod
    def get_products(cls, request):
        """
        Handle GET request and return paginated Product objects.
        This method retrieves all Product objects from the database, applies
        pagination based on the parameters in the request, and returns the paginated
        results. If the pagination parameters are not provided correctly or if an
        error occurs during serialization or database access, it returns a 400 Bad
        Request response with an appropriate error message.
        Args:
            request (HttpRequest): The incoming HTTP request object containing
                pagination parameters like page number, page size, etc.
        Returns:
            Response: A paginated response containing serialized Product objects
                or a 400 Bad Request response with an error message.
        """

        queryset = Product.objects.filter(collection__supplier__user=request.user)
        # Instantiate the paginator
        paginator = cls.pagination_class()
        # Apply pagination to the filtered queryset
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = ProductSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)