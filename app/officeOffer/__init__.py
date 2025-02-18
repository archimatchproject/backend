CDI = "CDI"
CDD = "CDD"
FREELANCE = "Freelance"
STAGE = "Stage"
ALTERNANCE = "Alternance"
TEMPS_PARTIEL = "Temps partiel"

CONTRACT_TYPES = [
    (CDI, "Contrat à Durée Indéterminée"),
    (CDD, "Contrat à Durée Déterminée"),
    (FREELANCE, "Freelance"),
    (STAGE, "Stage"),
    (ALTERNANCE, "Alternance"),
    (TEMPS_PARTIEL, "Temps partiel"),
]


LESS_THAN_6_MONTHS = "<6 mois"
SIX_TO_TWELVE_MONTHS = "6-12 mois"
ONE_TO_THREE_YEARS = "1-3 ans"
MORE_THAN_3_YEARS = ">3 ans"
INDETERMINED = "Indéterminé"

CONTRACT_DURATIONS = [
    (LESS_THAN_6_MONTHS, "Moins de 6 mois"),
    (SIX_TO_TWELVE_MONTHS, "6 mois - 1 an"),
    (ONE_TO_THREE_YEARS, "1 an - 3 ans"),
    (MORE_THAN_3_YEARS, "Plus de 3 ans"),
    (INDETERMINED, "Indéterminé"),
]


TN = "TN"
FR = "FR"
CA = "CA"
BE = "BE"
CH = "CH"
MA = "MA"
DZ = "DZ"
ONLINE = "ONLINE"

WORK_LOCATIONS = [
    (TN, "Tunisie"),
    (FR, "France"),
    (CA, "Canada"),
    (BE, "Belgique"),
    (CH, "Suisse"),
    (MA, "Maroc"),
    (DZ, "Algérie"),
    (ONLINE, "En ligne"),
]


LESS_THAN_1000 = "<1000 DT"
FROM_1000_TO_2000 = "1000-2000 DT"
FROM_2000_TO_3000 = "2000-3000 DT"
FROM_3000_TO_5000 = "3000-5000 DT"
FROM_5000_TO_8000 = "5000-8000 DT"
MORE_THAN_8000 = ">8000 DT"

SALARY_RANGES = [
    (LESS_THAN_1000, "Moins de 1000 DT"),
    (FROM_1000_TO_2000, "1000 DT - 2000 DT"),
    (FROM_2000_TO_3000, "2000 DT - 3000 DT"),
    (FROM_3000_TO_5000, "3000 DT - 5000 DT"),
    (FROM_5000_TO_8000, "5000 DT - 8000 DT"),
    (MORE_THAN_8000, "Plus de 8000 DT"),
]

ONE_TO_TWO_YEARS = "1-2"
THREE_TO_FIVE_YEARS = "3-5"
FIVE_TO_TEN_YEARS = "5-10"
TEN_PLUS = "10+"
NONE = "None"

EXPERIENCE_CHOICES = [
    (ONE_TO_TWO_YEARS, "1-2 ans"),
    (THREE_TO_FIVE_YEARS, "3-5 ans"),
    (FIVE_TO_TEN_YEARS, "5-10 ans"),
    (TEN_PLUS, "Plus de 10 ans"),
    (NONE, "Aucune expérience requise"),
]
