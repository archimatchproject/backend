from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from app.users.models.Architect import Architect
from app.selection.models.Selection import Selection  # Import Selection model

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
        name = "architect"

    class Django:
        model = Architect

    # Prepare methods to convert ManyToMany relationships into lists of IDs
    def prepare_project_categories(self, instance):
        return list(instance.project_categories.values_list("id", flat=True))

    def prepare_property_types(self, instance):
        return list(instance.property_types.values_list("id", flat=True))

    def prepare_work_types(self, instance):
        return list(instance.work_types.values_list("id", flat=True))

    def prepare_architectural_styles(self, instance):
        return list(instance.architectural_styles.values_list("id", flat=True))

    def prepare_needs(self, instance):
        return list(instance.needs.values_list("id", flat=True))

    def prepare_terrain_surfaces(self, instance):
        return list(instance.terrain_surfaces.values_list("id", flat=True))

    def prepare_work_surfaces(self, instance):
        return list(instance.work_surfaces.values_list("id", flat=True))

    def prepare_budgets(self, instance):
        return list(instance.budgets.values_list("id", flat=True))

    def prepare_preferred_locations(self, instance):
        return list(instance.preferred_locations.values_list("id", flat=True))

    def prepare_on_going_projects(self, instance):
        """Count the number of Selection objects referencing this Architect."""
        return Selection.objects.filter(architect=instance).count()

    def prepare_full_name(self, instance):
        """Return the full name of the Architect."""
        return f"{instance.user.first_name} {instance.user.last_name}"

    def prepare_city_coordinates(self, instance):
        if isinstance(instance.city_coordinates, dict):
            return {
                "lat": instance.city_coordinates.get("latitude"),
                "lon": instance.city_coordinates.get("longitude"),
            }
        return None  # Return None if coordinates are missing
