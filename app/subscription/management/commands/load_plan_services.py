"""
This module defines a custom Django management command to load a fixture file
and map permission codenames to their corresponding IDs before loading the data
into the database.
Classes:
    Command: A custom management command to load plan services fixture and map
             permission codenames to their IDs.
Methods:
    add_arguments(self, parser):
        Adds command-line arguments to the parser.
    handle(self, *args, **options):
        Handles the command execution, including reading the fixture file,
        mapping permission codenames to IDs, and loading the updated fixture data.
"""

from django.contrib.auth.models import Permission
from django.core.management import call_command
from django.core.management.base import BaseCommand

import yaml


class Command(BaseCommand):
    """
    Django management command to load plan services fixture and map permission codenames to their IDs.
    This command reads a fixture file, replaces permission codenames with their corresponding IDs,
    and then loads the updated fixture data into the database.
    Methods
    -------
    add_arguments(parser)
        Adds the 'fixture' argument to the command parser.
    handle(*args, **options)
        Handles the command execution, including reading the fixture file, mapping permission codenames
        to IDs, and loading the updated fixture data.
    Parameters
    ----------
    parser : ArgumentParser
        The argument parser instance to which the 'fixture' argument is added.
    *args : tuple
        Additional positional arguments.
    **options : dict
        Additional keyword arguments, including the 'fixture' argument which specifies the path to the fixture file.
    """

    help = "Load plan services fixture and map permission codenames to their IDs"

    def add_arguments(self, parser):
        """
        Adds custom command-line arguments to the parser.
        Args:
            parser (argparse.ArgumentParser): The argument parser instance to which custom arguments are added.
        Arguments:
            fixture (str): Path to the fixture file.
        """

        parser.add_argument("fixture", type=str, help="Path to the fixture file")

    def handle(self, *args, **options):
        """
        Handles the loading of plan services from a fixture file, replacing permission codenames
        with their corresponding IDs, and then loading the updated fixture data into the database.
        Args:
            *args: Variable length argument list.
            **options: Arbitrary keyword arguments. Expects a "fixture" key with the path to the fixture file.
        Raises:
            Exception: If there is an error loading the fixture data.
        The process includes:
        1. Loading all permissions from the database.
        2. Creating a mapping of permission codenames to their IDs.
        3. Reading the fixture file and replacing permission codenames with their corresponding IDs.
        4. Writing the updated fixture data to a temporary file.
        5. Loading the updated fixture data into the database.
        """

        fixture_path = options["fixture"]

        # Load permissions
        permissions = Permission.objects.all()
        permission_mapping = {f"{perm.content_type.app_label}.{perm.codename}": perm.pk for perm in permissions}
        # Read fixture file
        with open(fixture_path, "r") as file:
            fixture_data = yaml.safe_load(file)

        # Replace codenames with IDs
        for item in fixture_data:
            if "fields" in item and "permissions" in item["fields"]:
                item["fields"]["permissions"] = [
                    permission_mapping.get(codename, codename) for codename in item["fields"]["permissions"]
                ]

        # Write updated fixture to a temporary file
        temp_fixture_path = "updated_fixture.yaml"
        with open(temp_fixture_path, "w") as file:
            yaml.dump(fixture_data, file)

        # Load the updated fixture
        try:
            call_command("loaddata", temp_fixture_path)
            self.stdout.write(self.style.SUCCESS("Successfully loaded fixture data with permission mappings"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error loading fixture data: {e}"))
