# Generated by Django 4.2 on 2024-06-14 14:16

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AnnouncementWorkType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("header", models.CharField(default="", max_length=255)),
                ("description", models.CharField(default="", max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="LabeledIcon",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("label", models.CharField(default="", max_length=255)),
                ("icon", models.ImageField(upload_to="Icons/")),
            ],
        ),
        migrations.CreateModel(
            name="ProjectImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="images/")),
            ],
        ),
        migrations.CreateModel(
            name="ArchitectSpeciality",
            fields=[
                (
                    "labeledicon_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="announcement.labeledicon",
                    ),
                ),
            ],
            bases=("announcement.labeledicon",),
        ),
        migrations.CreateModel(
            name="PieceRenovate",
            fields=[
                (
                    "labeledicon_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="announcement.labeledicon",
                    ),
                ),
                ("number", models.PositiveSmallIntegerField(default=0)),
            ],
            bases=("announcement.labeledicon",),
        ),
        migrations.CreateModel(
            name="ProjectCategory",
            fields=[
                (
                    "labeledicon_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="announcement.labeledicon",
                    ),
                ),
            ],
            bases=("announcement.labeledicon",),
        ),
        migrations.CreateModel(
            name="ProjectExtension",
            fields=[
                (
                    "labeledicon_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="announcement.labeledicon",
                    ),
                ),
            ],
            bases=("announcement.labeledicon",),
        ),
        migrations.CreateModel(
            name="PropertyType",
            fields=[
                (
                    "labeledicon_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="announcement.labeledicon",
                    ),
                ),
                (
                    "project_category",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="property_types",
                        to="announcement.projectcategory",
                    ),
                ),
            ],
            bases=("announcement.labeledicon",),
        ),
        migrations.CreateModel(
            name="Need",
            fields=[
                (
                    "labeledicon_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="announcement.labeledicon",
                    ),
                ),
                (
                    "architect_speciality",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="needs",
                        to="announcement.architectspeciality",
                    ),
                ),
            ],
            bases=("announcement.labeledicon",),
        ),
        migrations.CreateModel(
            name="Announcement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        db_index=True, default=django.utils.timezone.now
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("address", models.CharField(max_length=255)),
                (
                    "city",
                    models.CharField(
                        choices=[
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
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "terrain_surface",
                    models.CharField(
                        choices=[
                            ("< 40m²", "< 40m²"),
                            ("40m² - 90m²", "40m² - 90m²"),
                            ("90m² - 200m²", "90m² - 200m²"),
                            ("200m² - 500m²", "200m² - 500m²"),
                            ("> 500m²", "> 500m²"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "work_surface",
                    models.CharField(
                        choices=[
                            ("< 40m²", "< 40m²"),
                            ("40m² - 90m²", "40m² - 90m²"),
                            ("90m² - 200m²", "90m² - 200m²"),
                            ("200m² - 500m²", "200m² - 500m²"),
                            ("> 500m²", "> 500m²"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "budget",
                    models.CharField(
                        choices=[
                            ("5.000dt - 10.000dt", "5.000dt - 10.000dt"),
                            ("20.000dt - 40.000dt", "20.000dt - 40.000dt"),
                            ("40.000dt - 120.000dt", "40.000dt - 120.000dt"),
                            ("120.000dt - 250.000dt", "120.000dt - 250.000dt"),
                            ("250.000dt - 500.000dt", "250.000dt - 500.000dt"),
                            ("> 500.000dt", "> 500.000dt"),
                        ],
                        max_length=50,
                    ),
                ),
                ("description", models.TextField()),
                (
                    "architectural_style",
                    models.CharField(
                        choices=[
                            ("Architecture Moderne", "Architecture Moderne"),
                            (
                                "Architecture Méditerranéenne",
                                "Architecture Méditerranéenne",
                            ),
                            (
                                "Architecture Contemporaine",
                                "Architecture Contemporaine",
                            ),
                            ("Architecture de Tourisme", "Architecture de Tourisme"),
                            ("Style Traditionnel", "Style Traditionnel"),
                            (
                                "Architecture Institutionnelle et Publique",
                                "Architecture Institutionnelle et Publique",
                            ),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.client"
                    ),
                ),
                (
                    "project_images",
                    models.ManyToManyField(
                        blank=True,
                        related_name="announcements",
                        to="announcement.projectimage",
                    ),
                ),
                (
                    "work_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="announcement.announcementworktype",
                    ),
                ),
                (
                    "architect_speciality",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="announcement.architectspeciality",
                    ),
                ),
                (
                    "needs",
                    models.ManyToManyField(
                        related_name="announcements", to="announcement.need"
                    ),
                ),
                (
                    "pieces_renovate",
                    models.ManyToManyField(
                        related_name="announcements", to="announcement.piecerenovate"
                    ),
                ),
                (
                    "project_category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="announcement.projectcategory",
                    ),
                ),
                (
                    "project_extensions",
                    models.ManyToManyField(
                        related_name="announcements", to="announcement.projectextension"
                    ),
                ),
                (
                    "property_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="announcement.propertytype",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
