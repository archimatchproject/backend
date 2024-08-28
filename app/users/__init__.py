USER_TYPE_CHOICES = [
    ("Architect", "Architect"),
    ("Client", "Client"),
    ("Admin", "Admin"),
    ("Supplier", "Supplier"),
]

PERMISSION_CODENAMES = {
    "manage_blog": {
        "permissions": [
            "add_blog",
            "change_blog",
            "delete_blog",
            "view_blog",
            "add_blogthematic",
            "change_blogthematic",
            "delete_blogthematic",
            "view_blogthematic",
            "add_blogtag",
            "change_blogtag",
            "delete_blogtag",
            "view_blogtag",
        ],
        "color": "#FFD700",
    },
    "manage_architect_request": {
        "permissions": [
            "add_architectrequest",
            "change_architectrequest",
            "delete_architectrequest",
            "view_architectrequest",
        ],
        "color": "#0C1E5B",
    },
    "manage_announcement": {
        "permissions": [
            "add_announcement",
            "change_announcement",
            "delete_announcement",
            "view_announcement",
        ],
        "color": "#11ABEC",
    },
    "manage_faq": {
        "permissions": [
            "add_faqthematic",
            "change_faqthematic",
            "delete_faqthematic",
            "view_faqthematic",
        ],
        "color": "#22ABEC",
    },
    "manage_guide": {
        "permissions": [
            "add_guidethematic",
            "change_guidethematic",
            "delete_guidethematic",
            "view_guidethematic",
            "add_guidearticle",
            "change_guidearticle",
            "delete_guidearticle",
            "view_guidearticle",
        ],
        "color": "#33ABEC",
    },
    "manage_subscription": {
        "permissions": [
            "add_tokenpack",
            "change_tokenpack",
            "delete_tokenpack",
            "view_tokenpack",
            "add_subscriptionplan",
            "change_subscriptionplan",
            "delete_subscriptionplan",
            "view_subscriptionplan",
        ],
        "color": "#123BEC",
    },
    "manage_payment": {
        "permissions": [
            "add_payment",
            "change_payment",
            "delete_payment",
            "view_payment",
        ],
        "color": "#ABCBEC",
    },
    "manage_legal_policy": {
        "permissions": [
            "add_privacypolicy",
            "change_privacypolicy",
            "delete_privacypolicy",
            "view_privacypolicy",
            "add_termsandconditions",
            "change_termsandconditions",
            "delete_termsandconditions",
            "view_termsandconditions",
        ],
        "color": "#ABCCCC",
    },
    "manage_reporting": {
        "permissions": [
            "add_architectreport",
            "change_architectreport",
            "delete_architectreport",
            "view_architectreport",
            "add_projectreport",
            "change_projectreport",
            "delete_projectreport",
            "view_projectreport",
            "add_reviewreport",
            "change_reviewreport",
            "delete_reviewreport",
            "view_reviewreport",
        ],
        "color": "#ABCCCC",
    },
}
CODENAME_TO_RIGHTS = {
    codename: right
    for right, data in PERMISSION_CODENAMES.items()
    for codename in data["permissions"]
}


PROJECT_COMPLEXITY_CHOICES = [
    ("Simple", "Simple"),
    ("Medium", "Medium"),
    ("Complex", "Complex"),
]

YEARS_EXPERIENCE_CHOICES = [
    ("1-3 years", "1-3 years"),
    ("3-5 years", "3-5 years"),
    ("5-8 years", "5-8 years"),
    ("8+ years", "8+ years"),
]

FAILED = "Failed"
PENDING = "Pending"
SUCCESS = "SUCCESS"

MEETING_STATUS_CHOICES = [
    (FAILED, FAILED),
    (PENDING, PENDING),
    (SUCCESS, SUCCESS),
]