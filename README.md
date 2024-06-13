# ArchiMatch-backend
## Installation Guide
### Install `pipenv`
If you don't have `pipenv` installed, you can install it using pip:
`pip install pipenv`
### Create a Virtual Environment and Install Dependencies
Inside your project directory, use pipenv to create a virtual environment and install project dependencies:
`pipenv install`
### Activate the Virtual Environment
`pipenv shell`
### Apply Migrations
### Apply the initial database migrations:
`python manage.py migrate`
### Create Superuser (Optional)
If your project uses Django's admin interface, you can create a superuser account to access the admin panel:
`python manage.py createsuperuser`
Run the Development Server
Start the Django development server:
`python manage.py runserver`