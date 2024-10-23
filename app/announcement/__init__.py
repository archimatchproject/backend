BUDGETS = [
    ("5.000dt - 10.000dt", "5.000dt - 10.000dt"),
    (
        "20.000dt - 40.000dt",
        "20.000dt - 40.000dt",
    ),
    (
        "40.000dt - 120.000dt",
        "40.000dt - 120.000dt",
    ),
    (
        "120.000dt - 250.000dt",
        "120.000dt - 250.000dt",
    ),
    (
        "250.000dt - 500.000dt",
        "250.000dt - 500.000dt",
    ),
    ("500.000dt - 1.000.000dt", "500.000dt - 1.000.000dt"),
    ("> 1.000.000dt", "> 1.000.000dt"),
]
CITIES = [
    ("Ariana", "Ariana"),
    ("Beja", "Beja"),
    ("Ben Arous", "Ben Arous"),
    ("Bizerte", "Bizerte"),
    ("Gabès", "Gabès"),
    ("Gafsa", "Gafsa"),
    ("Jendouba", "Jendouba"),
    ("Kairouan", "Kairouan"),
    ("Kasserine", "Kasserine"),
    ("Kebili", "Kebili"),
    ("Kef", "Kef"),
    ("Mahdia", "Mahdia"),
    ("Manouba", "Manouba"),
    ("Médenine", "Médenine"),
    ("Monastir", "Monastir"),
    ("Nabeul", "Nabeul"),
    ("Sfax", "Sfax"),
    ("Sidi Bouzid", "Sidi Bouzid"),
    ("Siliana", "Siliana"),
    ("Sousse", "Sousse"),
    ("Tataouine", "Tataouine"),
    ("Tozeur", "Tozeur"),
    ("Tunis", "Tunis"),
    ("Zaghouan", "Zaghouan"),
]

TERRAIN_SURFACES = [
    ("< 40m²", "< 40m²"),
    ("40m² - 90m²", "40m² - 90m²"),
    ("90m² - 200m²", "90m² - 200m²"),
    ("200m² - 500m²", "200m² - 500m²"),
    ("> 500m²", "> 500m²"),
]
WORK_SURFACES = [
    ("< 40m²", "< 40m²"),
    ("40m² - 90m²", "40m² - 90m²"),
    ("90m² - 200m²", "90m² - 200m²"),
    ("200m² - 500m²", "200m² - 500m²"),
    ("> 500m²", "> 500m²"),
]

# STEP5
PROPERTIES_NO_EXTERIOR = [4]  # Appartement
EXTERIOR_WORKTYPES = [2]  # Rénovation extérieure
# STEP6
NEW_CONSTRUCTION_WORKTYPES = [1, 5]  # Construction neuve , Surélévation
RENOVATION_WORKTYPES = [
    2,
    4,
    6,
]  # Rénovation extérieure , Rénovation intérieure , Aménagment de comble
NOT_ELIMINATE_STEP_PROPERTIES_STEP6 = [1, 3, 4]  # Maison,Villa,Appartement
# STEP10
NOT_ELIMINATE_STEP_PROPERTIES_STEP10 = [1, 2, 3]  # Maison,Immeuble,Villa


ACCEPTED = "Accepted"
REFUSED = "Refused"
PENDING = "Pending"
ANNOUNCEMENT_STATUS_CHOICES = [
    (ACCEPTED, ACCEPTED),
    (REFUSED, REFUSED),
    (PENDING, PENDING),
]
