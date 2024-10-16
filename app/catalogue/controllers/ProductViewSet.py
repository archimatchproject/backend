"""
ViewSet module for the Product model.
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser
from rest_framework.parsers import JSONParser
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated

from app.catalogue.models.Product import Product
from app.catalogue.serializers.ProductSerializer import ProductSerializer
from app.catalogue.services.ProductService import ProductService
from app.core.exception_handler import handle_service_exceptions
from app.core.response_builder import build_response
from rest_framework import status

class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Product model.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_permissions(self):
        """
        Get the permissions that the view requires.

        For `list` and `retrieve` actions (`GET` requests), no specific permissions
          are required.
        For `create`, `update`, `partial_update`, and `destroy` actions
        (`POST`, `PUT`, `PATCH`, `DELETE` requests),
        the view requires `IsAuthenticated` permissions.

        Returns:
            list: List of permission instances.
        """
        if self.action in [
            "list",
            "retrieve",
            "create",
            "update",
            "partial_update",
            "destroy",
            "update_display_status",
        ]:
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        """
        Filter the products by the supplier related to the currently authenticated user.
        """
        user = self.request.user
        return Product.objects.filter(collection__supplier__user=user)

    @handle_service_exceptions
    def create(self, request, *args, **kwargs):
        """
        Override the create method to use ProductService for handling the creation
        of a Product.
        """
        success,data = ProductService.create_product(request)
        return build_response(success=success, data=data, status=status.HTTP_201_CREATED)


    @handle_service_exceptions
    def update(self, request, *args, **kwargs):
        """
        Override the update method to use ProductService for handling the updating
          of a Product.
        """
        instance = self.get_object()
        success,data = ProductService.update_product(instance, request)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)


    @action(detail=True, methods=["PUT"])
    @handle_service_exceptions
    def update_display_status(self, request, pk=None):
        """
        Update the display status of a product.

        Args:
            request (Request): The request object containing the display status.
            pk (int): The primary key of the product.

        Returns:
            Response: The response object containing the result of the operation.
        """
        success,data = ProductService.update_display_status(request, pk)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)
    

    @action(detail=True, methods=["PUT"])
    @handle_service_exceptions
    def update_visibility(self, request, pk=None):
        """
        Update the visibility of a product.

        Args:
            request (Request): The request object containing the visibility.
            pk (int): The primary key of the product.

        Returns:
            Response: The response object containing the result of the operation.
        """
        success,data = ProductService.update_visibility(request, pk)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)
 

    def get(self, request):
        """
        Retrieve all Products.

        This method allows retrieval of all Supplier objects from the database.
        It delegates the actual retrieval to the `get_Products` class method
        of `ProductService`, which handles pagination and serialization.

        Args:
            self (SupplierViewSet): Instance of the SupplierViewSet class.
            request (Request): HTTP GET request object.

        Returns:
            Response: A paginated response containing serialized Supplier objects
                or an error response if there's a problem during retrieval.
        """
        return ProductService.get_products(request)
