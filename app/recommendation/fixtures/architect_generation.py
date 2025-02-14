import yaml
import random

# Define constants
NUM_ARCHITECTS = 50
START_ID = 800

# Define choices
CITIES = [
    "Ariana",
    "Beja",
    "Ben Arous",
    "Bizerte",
    "Gabès",
    "Gafsa",
    "Jendouba",
    "Kairouan",
    "Kasserine",
    "Kebili",
    "Kef",
    "Mahdia",
    "Manouba",
    "Médenine",
    "Monastir",
    "Nabeul",
    "Sfax",
    "Sidi Bouzid",
    "Siliana",
    "Sousse",
    "Tataouine",
    "Tozeur",
    "Tunis",
    "Zaghouan",
]

COORDINATES = {
    "Ariana": (36.862499, 10.195556),
    "Beja": (36.733333, 9.183333),
    "Ben Arous": (36.754166, 10.218889),
    "Bizerte": (37.27442, 9.87391),
    "Gabès": (33.881457, 10.098196),
    "Gafsa": (34.425, 8.784167),
    "Jendouba": (36.501136, 8.780239),
    "Kairouan": (35.6781, 10.0963),
    "Kasserine": (35.1676, 8.8365),
    "Kebili": (33.704387, 8.969034),
    "Kef": (36.17424, 8.70486),
    "Mahdia": (35.504722, 11.062222),
    "Manouba": (36.808056, 10.097222),
    "Médenine": (33.35495, 10.50548),
    "Monastir": (35.777986, 10.826165),
    "Nabeul": (36.451389, 10.736944),
    "Sfax": (34.740556, 10.760278),
    "Sidi Bouzid": (35.0382, 9.4849),
    "Siliana": (36.08497, 9.37082),
    "Sousse": (35.825603, 10.63699),
    "Tataouine": (32.92967, 10.45177),
    "Tozeur": (33.91968, 8.13352),
    "Tunis": (36.806389, 10.181667),
    "Zaghouan": (36.402778, 10.142222),
}

PROJECT_COMPLEXITY = ["Simple", "Medium", "Complex"]
YEARS_EXPERIENCE = ["1-3 years", "3-5 years", "5-8 years", "8+ years"]

# Define ranges for related fields
TOTAL_ARCHITECTURAL_STYLES = 11
TOTAL_BUDGETS = 7
TOTAL_PROJECT_CATEGORIES = 4
TOTAL_PROPERTY_TYPES = 13
TOTAL_TERRAIN_SURFACES = 5
TOTAL_WORK_SURFACES = 5
TOTAL_WORK_TYPES = 7
TOTAL_NEEDS = 23

# Generate data
architects_data = []

for i in range(NUM_ARCHITECTS):
    user_id = START_ID + i
    city = random.choice(CITIES)
    latitude, longitude = COORDINATES[city]

    user_entry = {
        "model": "users.ArchimatchUser",
        "pk": user_id,
        "fields": {
            "email": f"architect{user_id}@example.com",
            "username": f"architect{user_id}",
            "phone_number": f"+216{random.randint(10000000, 99999999)}",
            "user_type": "architect",
            "is_deleted": False,
            "is_suspended": False,
        },
    }

    architect_entry = {
        "model": "users.Architect",
        "pk": user_id,
        "fields": {
            "user": user_id,
            "address": f"Random Address {user_id}, Tunisia",
            "architect_identifier": f"ARCH{user_id}",
            "architect_speciality": random.randint(1, 3),
            "bio": "Experienced architect specializing in various styles.",
            "company_name": f"Architect Firm {user_id}",
            "company_logo": f"CompanyLogos/architect{user_id}.png",
            "project_complexity": random.choice(PROJECT_COMPLEXITY),
            "years_experience": random.choice(YEARS_EXPERIENCE),
            "city": city,
            "city_coordinates": {"latitude": latitude, "longitude": longitude},
            "project_categories": random.sample(
                range(1, TOTAL_PROJECT_CATEGORIES + 1), 2
            ),
            "property_types": random.sample(range(1, TOTAL_PROPERTY_TYPES + 1), 2),
            "work_types": random.sample(range(1, TOTAL_WORK_TYPES + 1), 2),
            "architectural_styles": random.sample(
                range(1, TOTAL_ARCHITECTURAL_STYLES + 1), 2
            ),
            "budgets": random.sample(range(1, TOTAL_BUDGETS + 1), 2),
            "preferred_locations": random.sample(range(1, 7), 2),
            "terrain_surfaces": random.sample(range(1, TOTAL_TERRAIN_SURFACES + 1), 2),
            "work_surfaces": random.sample(range(1, TOTAL_WORK_SURFACES + 1), 2),
            "needs": random.sample(range(1, TOTAL_NEEDS + 1), 2),
        },
    }

    architects_data.append(user_entry)
    architects_data.append(architect_entry)

# Save to YAML file
with open("app/recommendation/fixtures/architects.yaml", "w", encoding="utf-8") as file:
    yaml.dump(architects_data, file, allow_unicode=True, default_flow_style=False)

print("✅ Successfully generated 'architects.yaml' with 50 architects!")
