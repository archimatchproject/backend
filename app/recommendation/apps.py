from django.apps import AppConfig


class RecommendationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app.recommendation"

    def ready(self):
        import app.recommendation.signals
