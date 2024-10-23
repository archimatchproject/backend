# ArchiMatch-backend

## Installation Guide

### Prerequisites

Ensure you have Python==3.12 and pip installed on your system.

### Install `pipenv`

If you don't have `pipenv` installed, you can install it using pip:

```sh
pip install pipenv
```

### Create a Virtual Environment and Install Dependencies

Inside your project directory, use `pipenv` to create a virtual environment and install project dependencies:

```sh
pipenv install
```

### Activate the Virtual Environment

Activate the virtual environment:

```sh
pipenv shell
```

### Create Migrations

Create the initial database migrations:

```sh
python manage.py makemigrations --settings=project_core.django.dev
```

### Apply Migrations

Apply the initial database migrations:

```sh
python manage.py migrate --settings=project_core.django.dev
```

### Insert Fixtures

Apply the initial Model Instances:

```sh
python manage.py loaddata  --format=yaml architect_specialities.yaml announcement_needs.yaml project_categories.yaml property_types.yaml work_types.yaml renovation_pieces.yaml architectural_styles.yaml project_extensions.yaml supplier_specialities.yaml preferred_locations.yaml work_surfaces.yaml budgets.yaml terrain_surfaces.yaml decisions.yaml time_slots.yaml selection_settings.yaml
```

```sh
python manage.py load_plan_services app/subscription/fixtures/plan_services.yaml
```

### Create Superuser (Optional)

If your project uses Django's admin interface, you can create a superuser account to access the admin panel:

```sh
python manage.py createsuperuser --settings=project_core.django.dev
```

### Environment Variables

Create a `.env` file in the project root directory and add the following content:

```env
SECRET_KEY=**************************


DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### Run the Development Server

Start the Django development server with the specified settings:

```sh
python manage.py runserver --settings=project_core.django.dev
```
