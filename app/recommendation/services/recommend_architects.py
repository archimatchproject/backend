"""
This module provides services for recommending architects based on various criteria using Elasticsearch.
Functions:
    generate_match_boost(field_name, value, boost):
        Generates a function that boosts score if a specific field in the architect document contains a given value.
    generate_distance_score(projet, weight=25):
        Generates a function score that penalizes architects based on distance, using a weight to control its impact.
    generate_ongoing_projects_penalty(weight=15, scale=3):
    get_min_score_threshold(s, score_percentage):
    compute_architect_score(
        attribute_mapping=None,

"""

from elasticsearch_dsl import Q
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import FunctionScore

from app.announcement.models.Announcement import Announcement


def generate_match_boost(field_name, value, boost):
    """
    Generates a function that boosts score if a specific field in the architect document contains
    a given value.

    :param field_name: The field storing a list of IDs in the architect's Elasticsearch document.
    :param value: The ID from the Announcement model to match.
    :param boost: The score boost applied if a match is found.
    :return: A dictionary representing the function score query.
    """
    print(value)
    return {
        "filter": {"term": {field_name: value}},  # Match single ID against architect's list field
        "weight": boost,  # Apply boost if there's a match
    }


def generate_distance_score(projet, weight=25):
    """
    Generates a function score that penalizes architects based on distance,
    using a weight to control its impact.
    """
    return {
        "script_score": {
            "script": {
                "source": """
                    double distance_km = doc['city_coordinates'].arcDistance(params.lat, params.lon) / 1000;
                    double distance_score = 1 / (1 + (distance_km / 50));
                    return distance_score * params.weight;  // Apply weight multiplier
                """,
                "params": {
                    "lat": projet.city_coordinates["long"],
                    "lon": projet.city_coordinates["lat"],
                    "weight": weight,  # Apply weight multiplier (default = 20)
                },
            }
        }
    }


def generate_ongoing_projects_penalty(weight=15, scale=3):
    """
    Generates a penalty for ongoing projects to be used in an Elasticsearch script score.
    The penalty is calculated using a logarithmic function to ensure that the score does not drop to zero.
    The formula used is: 1 / (1 + log(1 + on_going_projects) * scale * weight).
    Args:
        weight (int, optional): The weight factor for the penalty. Default is 15.
        scale (int, optional): The scale factor for the penalty. Default is 3.
    Returns:
        dict: A dictionary representing the Elasticsearch script score with the penalty applied.
    """

    return {
        "script_score": {
            "script": {
                # Multiplicative penalty (prevents dropping score to 0)
                "source": """
                    double penalty = Math.log(1 + doc['on_going_projects'].value) * params.scale * params.weight;
                    return 1 / (1 + penalty);
                """,
                "params": {
                    "weight": weight,  # Default weight = 15
                    "scale": scale,  # Default scale = 3
                },
            }
        }
    }


def get_min_score_threshold(s, score_percentage):
    """
    Computes the maximum score from Elasticsearch results and calculates the minimum score threshold.

    :param s: The Elasticsearch Search object.
    :param score_percentage: The percentage of the max score to set as the minimum threshold.
    :return: The modified Search object with the min_score applied.
    """
    # 🔹 Get Max Score First
    s_max = s[:1]  # Get only top result
    response_max = s_max.execute()

    # Debugging max score before applying min score filter
    if response_max.hits:
        max_score = response_max.hits[0].meta.score
        print(f"✅ Max Score: {max_score}")
    else:
        max_score = 0
        print("⚠️ No results found, setting max_score to 0.")

    # Calculate Percentage Threshold
    min_score_threshold = max_score * (score_percentage / 100)
    print(f"✅ Min Score Threshold: {min_score_threshold}")

    # 🔹 Apply `min_score`
    if min_score_threshold > 0:
        s = s.extra(min_score=min_score_threshold)
    else:
        print("⚠️ Skipping min score filter because max_score is 0.")

    return s


def compute_architect_score(
    projet: Announcement,
    attributes=None,
    many_to_many_fields=None,
    weights=None,
    attribute_mapping=None,  # Pass mapping dynamically
    distance_limit=200,
    score_percentage=50,
    num_results=30,
):
    """
    Generic function to compute architect scores with dynamic parameters.

    :param projet: The project announcement instance.
    :param attributes: List of attributes to match for perfect match.
    :param many_to_many_fields: List of Many-to-Many fields to match dynamically.
    :param weights: Dictionary specifying weights for different scoring factors.
    :param attribute_mapping: Dictionary mapping Python attributes to Elasticsearch field names.
    :param distance_limit: Maximum allowed distance in km for architects.
    :param score_percentage: Minimum percentage of the max score to filter architects.
    :param num_results: Number of results to return.
    :return: List of architects ranked by score.
    """

    s = Search(using="default", index="architect")

    default_weights = {
        "distance": 25,
        "perfect_match": 10,
        "needs_per_match": 2,
        "on_going_projects": 5,
    }
    weights = weights or default_weights

    # 🔹 Use provided mapping or default mapping
    attribute_mapping = attribute_mapping or {
        "architectural_style": "architectural_styles",
        "work_type": "work_types",
        "project_category": "project_categories",
    }
    # 🔹 Filter by Architect Specialty
    s = s.filter("term", architect_speciality=projet.architect_speciality.id)

    # 🔹 Apply Distance Filter: Only architects within the specified km range
    s = s.filter(
        "geo_distance",
        distance=f"{distance_limit}km",
        city_coordinates={
            "lat": projet.city_coordinates["long"],
            "lon": projet.city_coordinates["lat"],
        },
    )

    # 🔹 Define Scoring Functions
    functions = []

    # Distance Score (Weighted)
    if projet.city_coordinates:
        functions.append(generate_distance_score(projet, weight=weights.get("distance")))

    # 🔹 Attribute-based Boosting
    attributes = attributes or ["architectural_style", "work_type", "project_category"]

    for attr in attributes:
        es_field = attribute_mapping.get(attr, attr)  # Use mapping if available
        value = getattr(projet, attr, None)
        if value:
            functions.append(generate_match_boost(es_field, value.id, boost=weights.get(attr, 5)))

    # 🔹 Perfect Match (Dynamic Version)
    perfect_match_conditions = []
    for attr in attributes:
        es_field = attribute_mapping.get(attr, attr)  # Use mapping if available
        value = getattr(projet, attr, None)
        if value:
            perfect_match_conditions.append({"term": {es_field: value.id}})

    if perfect_match_conditions:
        functions.append(
            {
                "filter": {
                    "bool": {
                        "must": perfect_match_conditions  # Dynamically generated must conditions
                    }
                },
                "weight": weights.get("perfect_match", 1),
            }
        )

    # 🔹 Many-to-Many Relationship Matching (Generic)
    many_to_many_fields = many_to_many_fields or ["needs"]  # Default to 'needs' if not provided

    for m2m_field in many_to_many_fields:
        related_objects = getattr(projet, m2m_field, None)
        if related_objects and related_objects.exists():
            for related_item in related_objects.all():
                functions.append(
                    {
                        "filter": {"term": {m2m_field: related_item.id}},
                        "weight": weights.get(
                            "needs_per_match", 2
                        ),  # Default weight for M2M matching
                    }
                )

    # 🔹 Ongoing Projects Penalty
    on_going_project = generate_ongoing_projects_penalty(
        weight=weights["on_going_projects"], scale=1
    )

    # 🔹 Apply FunctionScore Query (Sum Attributes)
    s = s.query(
        FunctionScore(
            query=Q("match_all"),
            functions=functions,
            score_mode="sum",
            boost_mode="multiply",
        )
    )

    # 🔹 Multiply by Distance and Ongoing Project Penalty
    s = s.query(
        FunctionScore(
            query=s.query,
            functions=[on_going_project],
            score_mode="multiply",
            boost_mode="multiply",
        )
    )

    # 🔹 Apply min score filtering
    s = get_min_score_threshold(s, score_percentage)

    s = s[:num_results]  # Fetch top `num_results`
    s = s.sort("_score")
    response = s.execute()
    print(f"✅ Number of architects returned: {len(response.hits)}")

    # Return Results
    return [
        {
            "id": a.id,
            "company_name": a.company_name,
            "needs": a.needs,
            "architectural_styles": a.architectural_styles,
            "work_types": a.work_types,
            "project_categories": a.project_categories,
            "city": a.city,
            "on_going_projects": a.on_going_projects,
            "property_types": a.property_types,
            "score": a.meta.score,
        }
        for a in response
    ]
