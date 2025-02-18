CONTRACT_TYPES = [
    ("CDI", "Contrat à Durée Indéterminée"),
    ("CDD", "Contrat à Durée Déterminée"),
    ("Freelance", "Freelance"),
    ("Stage", "Stage"),
    ("Alternance", "Alternance"),
    ("Temps partiel", "Temps partiel"),
]

CONTRACT_DURATIONS = [
    ("<6 mois", "Moins de 6 mois"),
    ("6-12 mois", "6 mois - 1 an"),
    ("1-3 ans", "1 an - 3 ans"),
    (">3 ans", "Plus de 3 ans"),
    ("Indéterminé", "Indéterminé"),
]

WORK_LOCATIONS = [
    ("Tunisie", "Tunisie"),
    ("France", "France"),
    ("Canada", "Canada"),
    ("Belgique", "Belgique"),
    ("Suisse", "Suisse"),
    ("Maroc", "Maroc"),
    ("Algérie", "Algérie"),
    ("En ligne", "En ligne"),
]

SALARY_RANGES = [
    ("<1000 DT", "Moins de 1000 DT"),
    ("1000-2000 DT", "1000 DT - 2000 DT"),
    ("2000-3000 DT", "2000 DT - 3000 DT"),
    ("3000-5000 DT", "3000 DT - 5000 DT"),
    ("5000-8000 DT", "5000 DT - 8000 DT"),
    (">8000 DT", "Plus de 8000 DT"),
]

EXPERIENCE_CHOICES = [
    ("1-2", "1-2 ans"),
    ("3-5", "3-5 ans"),
    ("5-10", "5-10 ans"),
    ("10+", "Plus de 10 ans"),
    ("None", "Aucune expérience requise"),
]
