"""
Module defining the Offer model.

This module contains the Offer class, which represents a job offer in the application.
"""

from app.core.models.BaseModel import BaseModel
from django.db import models
from app.users.models.Office import Office
from app.core.models.ArchitectSpeciality import ArchitectSpeciality
from app.officeOffer import CONTRACT_TYPES
from app.officeOffer import CONTRACT_DURATIONS
from app.officeOffer import WORK_LOCATIONS
from app.officeOffer import SALARY_RANGES
from app.officeOffer import EXPERIENCE_CHOICES
from app.core.models.ProjectCategory import ProjectCategory
from app.core.models.ArchitecturalStyle import ArchitecturalStyle
from app.officeOffer.models.TechnicalSkill import TechnicalSkill
from app.officeOffer.models.SoftwareSkill import SoftwareSkill


class Offer(BaseModel):
    """
    Model representing a job offer for an architect.

    Attributes:
        office (ForeignKey): The office offering the job.
        architect_speciality (ForeignKey): The specialization required for the position.
        offer_title (CharField): The title of the job offer.
        contract_type (CharField): Type of the contract (e.g., CDI, CDD, etc.).
        contract_duration (CharField): Duration of the contract.
        work_location (CharField): Location where the work will be performed 
        (e.g., country or online).
        start_date (DateField): The start date for the job.
        salary_range (CharField): The salary range for the position.
        project_category (ForeignKey): The type/category of the projects the architect will work on.
        architectural_style (ForeignKey): Preferred architectural style for the projects.
        office_description (TextField): A description of the office offering the job.
        offer_description (TextField): Detailed description of the job offer.
        searched_profile (TextField): Desired profile or qualifications for the candidate.
        technical_skills (ManyToManyField): List of technical skills required for the job.
        software_skills (ManyToManyField): List of software skills required for the job.
        experience_required (CharField): Required experience level for the position.
    """
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    architect_speciality = models.ForeignKey(ArchitectSpeciality, on_delete=models.CASCADE)
    offer_title = models.CharField(max_length=255, blank=False, null=False)
    contract_type = models.CharField(
        max_length=20, choices=CONTRACT_TYPES, default="CDI", blank=False, null=False)
    contract_duration = models.CharField(max_length=255, choices=CONTRACT_DURATIONS, blank=False)
    work_location = models.CharField(
        max_length=20, choices=WORK_LOCATIONS, default="Tunisie",
        blank=False, null=False)
    start_date = models.DateField(
        blank=False,
        null=False
    )
    salary_range = models.CharField(
        max_length=15,
        choices=SALARY_RANGES,
        default="1000-2000 DT",
        blank=False,
        null=False
    )
    project_category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE)
    architectural_style = models.ForeignKey(
        ArchitecturalStyle,
        on_delete=models.SET_NULL,
        related_name="offers_architectural_style",
        null=True,
        blank=True,
    )
    office_description = models.TextField(blank=False, null=False)
    offer_description = models.TextField(blank=False, null=False)
    searched_profile = models.TextField(blank=False, null=False)
    technical_skills = models.ManyToManyField(TechnicalSkill, blank=True)
    software_skills = models.ManyToManyField(SoftwareSkill, blank=True)
    experience_required = models.CharField(
        max_length=10,
        choices=EXPERIENCE_CHOICES,
        blank=True,
        null=True,
    )