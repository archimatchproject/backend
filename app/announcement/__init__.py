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


COORDINATES = [
    ("Ariana", (10.195556, 36.862499)),
    ("Beja", (9.183333, 36.733333)),
    ("Ben Arous", (10.218889, 36.754166)),
    ("Bizerte", (9.87391, 37.27442)),
    ("Gabès", (10.098196, 33.881457)),
    ("Gafsa", (8.784167, 34.425)),
    ("Jendouba", (8.780239, 36.501136)),
    ("Kairouan", (10.0963, 35.6781)),
    ("Kasserine", (8.8365, 35.1676)),
    ("Kebili", (8.969034, 33.704387)),
    ("Kef", (8.70486, 36.17424)),
    ("Mahdia", (11.062222, 35.504722)),
    ("Manouba", (10.097222, 36.808056)),
    ("Médenine", (10.50548, 33.35495)),
    ("Monastir", (10.826165, 35.777986)),
    ("Nabeul", (10.736944, 36.451389)),
    ("Sfax", (10.760278, 34.740556)),
    ("Sidi Bouzid", (9.4849, 35.0382)),
    ("Siliana", (9.37082, 36.08497)),
    ("Sousse", (10.63699, 35.825603)),
    ("Tataouine", (10.45177, 32.92967)),
    ("Tozeur", (8.13352, 33.91968)),
    ("Tunis", (10.181667, 36.806389)),
    ("Zaghouan", (10.142222, 36.402778)),
]
