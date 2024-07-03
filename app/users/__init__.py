USER_TYPE_CHOICES = [
    ("Architect", "Architect"),
    ("Client", "Client"),
    ("Admin", "Admin"),
    ("Supplier", "Supplier"),
]

PERMISSION_CODENAMES = {
    "manage_blog": [
        "add_blog",
        "change_blog",
        "delete_blog",
        "view_blog",
    ],
    "manage_architect_request": [
        "add_architectrequest",
        "change_architectrequest",
        "delete_architectrequest",
        "view_architectrequest",
    ],
}

APPEARANCES = [
    ("Petite", "Petite"),
    ("Grande", "Grande"),
]
