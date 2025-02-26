"""
Category model that represents a category in the application.
Attributes:
    title (CharField): The title of the category, which must be unique and have a maximum length of 100 characters.
Meta:
    verbose_name (str): The human-readable name of the model in singular form.
    verbose_name_plural (str): The human-readable name of the model in plural form.
Methods:
    __str__(): Returns the string representation of the category, which is the title.

"""

from django.db import models

from app.core.models.BaseModel import BaseModel


class Category(BaseModel):
    """
    Category model that represents a category in the application.
    Attributes:
        title (CharField): The title of the category, which must be unique and have a maximum length of 100 characters.
    Meta:
        verbose_name (str): The human-readable name of the model in singular form.
        verbose_name_plural (str): The human-readable name of the model in plural form.
    Methods:
        __str__(): Returns the string representation of the category, which is the title.

    """

    title = models.CharField(max_length=100, unique=True)

    class Meta:
        """
        Meta class to define metadata for the Category model.
        Attributes:
            verbose_name (str): Human-readable name for the model.
            verbose_name_plural (str): Human-readable plural name for the model.
        """

        """ """

        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        """
        Returns a string representation of the Category instance.
        Returns:
            str: The title of the category.
        """

        return self.title
