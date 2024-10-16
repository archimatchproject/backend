"""
Admin registration module for the Product and ProductImage models.
"""

from django.contrib import admin

from app.catalogue.models.Product import Product
from app.catalogue.models.ProductImage import ProductImage


class ProductImageInline(admin.TabularInline):
    """
    Inline admin interface for ProductImage.
    """

    model = ProductImage
    extra = 4


class ProductAdmin(admin.ModelAdmin):
    """
    Admin interface for Product.
    """

    list_display = ("name", "price", "collection")
    search_fields = ("name", "collection__title")
    inlines = [ProductImageInline]


admin.site.register(Product, ProductAdmin)
