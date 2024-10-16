import yaml
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Load plan services fixture and map permission codenames to their IDs'

    def add_arguments(self, parser):
        parser.add_argument('fixture', type=str, help='Path to the fixture file')

    def handle(self, *args, **options):
        fixture_path = options['fixture']

        # Load permissions
        permissions = Permission.objects.all()
        permission_mapping = {f"{perm.content_type.app_label}.{perm.codename}": perm.pk for perm in permissions}
        # Read fixture file
        with open(fixture_path, 'r') as file:
            fixture_data = yaml.safe_load(file)

        # Replace codenames with IDs
        for item in fixture_data:
            if 'fields' in item and 'permissions' in item['fields']:
                item['fields']['permissions'] = [
                    permission_mapping.get(codename, codename)
                    for codename in item['fields']['permissions']
                ]

        # Write updated fixture to a temporary file
        temp_fixture_path = 'updated_fixture.yaml'
        with open(temp_fixture_path, 'w') as file:
            yaml.dump(fixture_data, file)

        # Load the updated fixture
        try:
            call_command('loaddata', temp_fixture_path)
            self.stdout.write(self.style.SUCCESS('Successfully loaded fixture data with permission mappings'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading fixture data: {e}'))
