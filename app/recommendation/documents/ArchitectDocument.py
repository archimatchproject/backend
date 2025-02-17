"""
This module defines the Elasticsearch document for the Architect model using django_elasticsearch_dsl.
Classes:
    ArchitectDocument: An Elasticsearch document for the Architect model, including fields and methods to
    prepare data for indexing.
Attributes:
    architect_index (Index): The Elasticsearch index for the Architect model, with settings for number of shards and
    replicas.
Methods:
    prepare_project_categories(instance): Prepares a list of project category IDs for the given instance.
    prepare_property_types(instance): Prepares a list of property type IDs from the given instance.
    prepare_work_types(instance): Prepares a list of work type IDs from the given instance.
    prepare_architectural_styles(instance): Prepares a list of architectural style IDs from the given instance.
    prepare_needs(instance): Prepares a list of need IDs from the given instance.
    prepare_terrain_surfaces(instance): Prepares a list of terrain surface IDs from the given instance.
    prepare_work_surfaces(instance): Prepares a list of work surface IDs from the given instance.
    prepare_budgets(instance): Prepares a list of budget IDs associated with the given instance.
    prepare_preferred_locations(instance): Prepares a list of preferred location IDs for the given instance.
    prepare_on_going_projects(instance): Counts the number of Selection objects referencing the given architect
    instance.
    prepare_full_name(instance): Prepares the full name of the architect by combining first name and last name.
    prepare_city_coordinates(instance): Prepares a dictionary with city coordinates from the given instance.
"""

from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl import Index
from django_elasticsearch_dsl import fields
from django_elasticsearch_dsl.registries import registry

from app.selection.models.Selection import Selection
from app.users.models.Architect import Architect


# Define Elasticsearch index
architect_index = Index("architect")
architect_index.settings(number_of_shards=1, number_of_replicas=1)


@registry.register_document
class ArchitectDocument(Document):
    """
    Elasticsearch document for the Architect model.
    """

    id = fields.IntegerField()
    user_id = fields.IntegerField(attr="user.id")
    full_name = fields.TextField()
    bio = fields.TextField()
    company_name = fields.TextField()
    architect_identifier = fields.KeywordField()
    architect_speciality = fields.IntegerField(attr="architect_speciality.id")
    project_complexity = fields.KeywordField()
    years_experience = fields.KeywordField()
    city = fields.KeywordField()
    city_coordinates = fields.GeoPointField()

    # Multi-value fields (ManyToMany relationships)
    project_categories = fields.ListField(fields.IntegerField())
    property_types = fields.ListField(fields.IntegerField())
    work_types = fields.ListField(fields.IntegerField())
    architectural_styles = fields.ListField(fields.IntegerField())
    needs = fields.ListField(fields.IntegerField())
    terrain_surfaces = fields.ListField(fields.IntegerField())
    work_surfaces = fields.ListField(fields.IntegerField())
    budgets = fields.ListField(fields.IntegerField())

    preferred_locations = fields.ListField(fields.IntegerField())

    on_going_projects = fields.IntegerField()

    class Index:
        """
        Index class representing the index configuration for the "architect" documents.
        Attributes:
            name (str): The name of the index, set to "architect".
        """

        name = "architect"

    class Django:
        """
        Django class for handling the Architect model.
        Attributes:
            model (Architect): The model associated with this class.
        """

        model = Architect

    # Prepare methods to convert ManyToMany relationships into lists of IDs
    def prepare_project_categories(self, instance):
        """
        Prepares a list of project category IDs for the given instance.
        Args:
            instance: The instance containing project categories.
        Returns:
            list: A list of project category IDs.
        """

        return list(instance.project_categories.values_list("id", flat=True))

    def prepare_property_types(self, instance):
        """
        Prepares a list of property type IDs from the given instance.
        Args:
            instance: An object that contains property types.
        Returns:
            list: A list of property type IDs.
        """

        return list(instance.property_types.values_list("id", flat=True))

    def prepare_work_types(self, instance):
        """
        Prepares a list of work type IDs from the given instance.
        Args:
            instance: An object that contains work types.
        Returns:
            list: A list of work type IDs.
        """

        return list(instance.work_types.values_list("id", flat=True))

    def prepare_architectural_styles(self, instance):
        """
        Prepares a list of architectural style IDs from the given instance.
        Args:
            instance: An object that contains architectural styles.
        Returns:
            list: A list of architectural style IDs.
        """

        return list(instance.architectural_styles.values_list("id", flat=True))

    def prepare_needs(self, instance):
        """
        Prepares a list of need IDs from the given instance.
        Args:
            instance: An object that contains a 'needs' attribute, which is expected to be a
                      queryset or similar object with a 'values_list' method.
        Returns:
            list: A list of IDs corresponding to the needs of the instance.
        """

        return list(instance.needs.values_list("id", flat=True))

    def prepare_terrain_surfaces(self, instance):
        """
        Prepares a list of terrain surface IDs from the given instance.
        Args:
            instance: An object that contains terrain surfaces.
        Returns:
            list: A list of terrain surface IDs.
        """

        return list(instance.terrain_surfaces.values_list("id", flat=True))

    def prepare_work_surfaces(self, instance):
        """
        Prepares a list of work surface IDs from the given instance.
        Args:
            instance: An object that contains work surfaces.
        Returns:
            list: A list of work surface IDs.
        """

        return list(instance.work_surfaces.values_list("id", flat=True))

    def prepare_budgets(self, instance):
        """
        Prepares a list of budget IDs associated with the given instance.
        Args:
            instance: The instance containing budget information.
        Returns:
            list: A list of budget IDs.
        """

        return list(instance.budgets.values_list("id", flat=True))

    def prepare_preferred_locations(self, instance):
        """
        Prepares a list of preferred location IDs for the given instance.
        Args:
            instance: The instance containing preferred locations.
        Returns:
            list: A list of preferred location IDs.
        """

        return list(instance.preferred_locations.values_list("id", flat=True))

    def prepare_on_going_projects(self, instance):
        """
        Count the number of Selection objects referencing this Architect.
        Args:
            instance (Architect): The architect instance for which to count the ongoing projects.
        Returns:
            int: The number of Selection objects that reference the given architect instance.
        """

        """Count the number of Selection objects referencing this Architect."""
        return Selection.objects.filter(architect=instance).count()

    def prepare_full_name(self, instance):
        """
        Prepare the full name of the architect.
        Args:
            instance (object): An instance containing user information.
        Returns:
            str: The full name of the architect, combining first name and last name.
        """

        """Return the full name of the Architect."""
        return f"{instance.user.first_name} {instance.user.last_name}"

    def prepare_city_coordinates(self, instance):
        """
        Prepares a dictionary with city coordinates from the given instance.
        Args:
            instance: An object that contains city coordinates in a dictionary format.
        Returns:
            dict: A dictionary with 'lat' and 'lon' keys if the coordinates are present.
            None: If the coordinates are missing or not in the expected format.
        """

        if isinstance(instance.city_coordinates, dict):
            return {
                "lat": instance.city_coordinates.get("latitude"),
                "lon": instance.city_coordinates.get("longitude"),
            }
        return None  # Return None if coordinates are missing
