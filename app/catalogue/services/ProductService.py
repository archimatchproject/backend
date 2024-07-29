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
from rest_framework.response import Response

from app.catalogue.models.Product import Product
from app.catalogue.models.ProductImage import ProductImage
from app.catalogue.serializers.ProductSerializer import ProductSerializer


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

    @classmethod
    def create_product(cls, request, data):
        """
        Handles validation and creation of a new Product.

        Args:
            request (Request): The request object containing the authenticated user.
            data (dict): The validated data for creating a Product instance.

        Returns:
            Response: The response object containing the result of the operation.
        """
        serializer = ProductSerializer(data=data)
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
    def update_product(cls, instance, request, data):
        """
        Handles validation and updating of an existing Product.

        Args:
            instance (Product): The existing Product instance.
            request (Request): The request object containing the authenticated user.
            data (dict): The validated data for updating a Product instance.

        Returns:
            Response: The response object containing the result of the operation.
        """
        serializer = ProductSerializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        images_data = request.FILES.getlist("product_images")

        try:
            with transaction.atomic():
                # Update Product instance
                instance.name = validated_data.get("name", instance.name)
                instance.price = validated_data.get("price", instance.price)
                instance.collection = validated_data.get("collection", instance.collection)
                instance.description = validated_data.get("description", instance.description)
                instance.save()

                if images_data:
                    instance.product_images.all().delete()
                    for image_data in images_data:
                        ProductImage.objects.create(product=instance, image=image_data)

                return Response(
                    ProductSerializer(instance).data,
                    status=status.HTTP_200_OK,
                )
        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error updating product: {str(e)}")
