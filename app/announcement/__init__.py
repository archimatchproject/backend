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
    ("Tunis", "Tunis"),
    ("Sfax", "Sfax"),
    ("Sousse", "Sousse"),
    ("Ettadhamen", "Ettadhamen"),
    ("Kairouan", "Kairouan"),
    ("Gabès", "Gabès"),
    ("Bizerte", "Bizerte"),
    ("Ariana", "Ariana"),
    ("Gafsa", "Gafsa"),
    ("Monastir", "Monastir"),
    ("Médenine", "Médenine"),
    ("Beja", "Beja"),
    ("Jendouba", "Jendouba"),
    ("Nabeul", "Nabeul"),
    ("Kasserine", "Kasserine"),
    ("Sidi Bouzid", "Sidi Bouzid"),
    ("Tozeur", "Tozeur"),
    ("Siliana", "Siliana"),
    ("Tataouine", "Tataouine"),
    ("Kebili", "Kebili"),
    ("Ben Arous", "Ben Arous"),
    ("Mahdia", "Mahdia"),
    ("Manouba", "Manouba"),
    ("Zaghouan", "Zaghouan"),
    ("Kef", "Kef"),
    ("Moknine", "Moknine"),
    ("Menzel Temime", "Menzel Temime"),
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
RENOVATION_WORKTYPES = [2, 4]  # Rénovation extérieure , Rénovation intérieure
NOT_ELIMINATE_STEP_PROPERTIES_STEP6 = [1, 3, 4]  # Maison,Villa,Appartement
# STEP10
NOT_ELIMINATE_STEP_PROPERTIES_STEP10 = [1, 2, 3]  # Maison,Immeuble,Villa

ANNOUNCEMENT_STATUS_CHOICES = [
    ("Accepted", "Accepted"),
    ("Refused", "Refused"),
    ("Pending", "Pending"),
]
