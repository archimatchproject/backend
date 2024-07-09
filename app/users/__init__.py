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
}

APPEARANCES = [
    ("Petite", "Petite"),
    ("Grande", "Grande"),
]
