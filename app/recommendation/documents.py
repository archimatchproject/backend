"""
Module for defining the Elasticsearch document for Announcements.
This module contains the `AnnouncementDocument` class which maps the fields of the `Announcement`
Django model
to the corresponding fields in an Elasticsearch index.
Classes:
    AnnouncementDocument: Defines the Elasticsearch document for the Announcement model.
"""

from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl import Index
from django_elasticsearch_dsl import fields
from django_elasticsearch_dsl.registries import registry

from app.announcement.models.Announcement import Announcement


# Define Elasticsearch index
announcement_index = Index("announcement")

# Settings for the index (optional)
announcement_index.settings(number_of_shards=1, number_of_replicas=1)


@registry.register_document
class AnnouncementDocument(Document):
    """
    Elasticsearch document for the Announcement model.
    Attributes:
        id (IntegerField): The unique identifier for the announcement.
        client_id (IntegerField): The unique identifier for the client.
        architect_speciality (IntegerField): The speciality of the architect.
        needs (KeywordField): The needs associated with the announcement.
        project_category (IntegerField): The category of the project.
        property_type (IntegerField): The type of the property.
        work_type (IntegerField): The type of work to be done.
        address (TextField): The address of the project.
        city (KeywordField): The city where the project is located.
        terrain_surface (KeywordField): The surface area of the terrain.
        work_surface (KeywordField): The surface area of the work.
        budget (KeywordField): The budget for the project.
        description (TextField): The description of the project.
        architectural_style (IntegerField): The architectural style of the project.
        project_extensions (KeywordField): The extensions of the project.
        number_floors (IntegerField): The number of floors in the project.
        status (KeywordField): The status of the announcement.
        suggested_at (DateField): The date the announcement was suggested.
        is_blocked (BooleanField): Indicates if the announcement is blocked.
        is_broadcasted (BooleanField): Indicates if the announcement is broadcasted.
    Inner Classes:
        Index: Defines the index name in Elasticsearch.
        Django: Links the document to the Django model.
    """

    id = fields.IntegerField()
    client_id = fields.IntegerField()

    architect_speciality_id = fields.IntegerField(attr="architect_speciality.id")
    project_category_id = fields.IntegerField(attr="project_category.id")
    property_type_id = fields.IntegerField(attr="property_type.id")
    work_type_id = fields.IntegerField(attr="work_type.id")
    architectural_style_id = fields.IntegerField(attr="architectural_style.id")

    # Corrected List Fields
    needs_ids = fields.ListField(fields.IntegerField())
    project_extensions_ids = fields.ListField(fields.IntegerField())

    # Other fields
    address = fields.TextField()
    city = fields.KeywordField()
    budget = fields.KeywordField()
    description = fields.TextField()
    number_floors = fields.IntegerField()
    is_blocked = fields.BooleanField()
    is_broadcasted = fields.BooleanField()
    suggested_at = fields.DateField()
    terrain_surface = fields.KeywordField()
    status = fields.KeywordField()

    class Index:
        """
        Index class representing the index configuration for the "announcement" documents.
        Attributes:
            name (str): The name of the index.
        """

        name = "announcement"

    class Django:
        """
        Django class for handling the Announcement model.
        Attributes:
            model (Announcement): The model associated with this class.
        """

        model = Announcement

    def prepare_needs_ids(self, instance):
        """Convert ManyToMany 'needs' to a list of IDs"""
        return list(instance.needs.values_list("id", flat=True))

    def prepare_project_extensions_ids(self, instance):
        """Convert ManyToMany 'project_extensions' to a list of IDs"""
        return list(instance.project_extensions.values_list("id", flat=True))
