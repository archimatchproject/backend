def generate_recommendation_choices(min_value, max_value, label_template, gap=1):
    """Generate a list of choices with labels and values based on a gap."""
    return [
        {"id": idx, "label": label_template.format(value=value), "value": value}
        for idx, value in enumerate(range(min_value, max_value + 1, gap), start=1)
    ]


# Choices for RecommendationSettings attributes with gaps
DISTANCE_WEIGHT_CHOICES = generate_recommendation_choices(
    5, 30, "{value} points", gap=5
)
PERFECT_MATCH_WEIGHT_CHOICES = generate_recommendation_choices(
    1, 10, "{value} points", gap=1
)
ONGOING_PROJECTS_WEIGHT_CHOICES = generate_recommendation_choices(
    1, 10, "{value} points", gap=2
)
DISTANCE_LIMIT_CHOICES = generate_recommendation_choices(50, 400, "{value} km", gap=50)
SCORE_PERCENTAGE_CHOICES = generate_recommendation_choices(10, 100, "{value}%", gap=10)
NUM_RESULTS_CHOICES = generate_recommendation_choices(
    5, 50, "Top {value} results", gap=5
)

# Choices for RecommendationSettings attributes with gaps
ARCHITECTURAL_STYLE_CHOICES = generate_recommendation_choices(
    1, 20, "{value} points", gap=1
)
WORK_TYPE_CHOICES = generate_recommendation_choices(1, 15, "{value} points", gap=1)
PROJECT_CATEGORY_CHOICES = generate_recommendation_choices(
    1, 15, "{value} points", gap=1
)
PROPERTY_TYPES_CHOICES = generate_recommendation_choices(1, 10, "{value} points", gap=1)
NEEDS_PER_MATCH_CHOICES = generate_recommendation_choices(1, 5, "{value} points", gap=1)
