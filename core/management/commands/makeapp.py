import os

from django.core.management.base import BaseCommand

"""
Custom app structure
app_name/
    ├── api/
    │   ├── __init__.py
    │   └── v1/
    │       ├── __init__.py
    │       ├── views/
    │       │   └── __init__.py
    │       ├── serializers/
    │       │   └── __init__.py
    │       ├── integrations
    │       └── urls.py
    ├── urls.py
    ├── utils/
    │   └── __init__.py
    ├── automations/
    │   └── __init.py
    ├── models/
    │   └── __init__.py
    ├── tests/
    │   └── __init__.py
    ├── fixtures/
    │   └── settings.json
    ├── scripts/
    │   └── __init__.py
    ├── constants/
    │   └── generic.py
    ├── services/
    │   └── hubspot.py
    ├── migrations
    ├── admin.py
    ├── apps.py
    └── urls.py
"""


class Command(BaseCommand):
    help = "Creates a Django app with Custom standard directory structure"

    def add_arguments(self, parser):
        parser.add_argument("name", type=str, help="Name of the application")
        parser.add_argument(
            "directory", nargs="?", help="Optional destination directory"
        )

    def handle(self, *args, **options):
        app_name = options["name"]
        target_dir = options.get("directory") or app_name

        # Create the main app directory
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        directories = [
            "api",
            "api/v1",
            "api/v1/views",
            "api/v1/serializers",
            "api/v1/integrations",
            "utils",
            "automations",
            "models",
            "tasks",
            "tests",
            "fixtures",
            "scripts",
            "constants",
            "services",
            "migrations",
        ]

        # Create directories
        for directory in directories:
            full_path = os.path.join(target_dir, directory)
            os.makedirs(full_path, exist_ok=True)

        files_to_create = {
            # Python __init__.py files
            "__init__.py": "",
            "api/__init__.py": "",
            "api/v1/__init__.py": "",
            "api/v1/views/__init__.py": "",
            "api/v1/serializers/__init__.py": "",
            "api/v1/integrations/__init__.py": "",
            "utils/__init__.py": "",
            "automations/__init__.py": "",
            "models/__init__.py": "",
            "migrations/__init__.py": "",
            "tests/__init__.py": "",
            "scripts/__init__.py": "",
            "services/__init__.py": "",
            "tasks/__init__.py": "",
            # Main app files
            "apps.py": self.get_apps_py_content(app_name),
            "admin.py": self.get_admin_py_content(),
            "urls.py": self.get_main_urls_py_content(app_name),
            # API URLs
            "api/v1/urls.py": self.get_api_urls_py_content(),
            # Constants
            "constants/__init__.py": "",
            "constants/generic.py": "# Generic constants for the app",
            # Fixtures
            "fixtures/settings.json": "{}",
        }

        # Create files
        for file_path, content in files_to_create.items():
            full_path = os.path.join(target_dir, file_path)
            with open(full_path, "w") as f:
                f.write(content)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created app "{app_name}" with Custom app structure'
            )
        )

    def get_apps_py_content(self, app_name):
        return f"""from django.apps import AppConfig


                class {app_name.capitalize()}Config(AppConfig):
                    default_auto_field = 'django.db.models.BigAutoField'
                    name = '{app_name}'
            """

    def get_admin_py_content(self):
        return """from django.contrib import admin

                # Register your models here.
            """

    def get_main_urls_py_content(self, app_name):
        return f"""# Main URLs for the {app_name} app,
            from django.urls import path, include

            urlpatterns = [
                path('api/v1/', include('{app_name}.api.v1.urls')),
            ]
        """

    def get_api_urls_py_content(self):
        return """# This includes version 1 (v1) apis for the app
            from django.urls import path, include
            from rest_framework.routers import DefaultRouter

            router = DefaultRouter()
            # Register your viewsets here
            # router.register(r'example', views.ExampleViewSet)

            urlpatterns = [
                path('', include(router.urls)),
                # Add your additional version 1 API endpoints here
            ]
            """


# to run this command
# python manage.py makeapp <app_name>
# for optional_directory add <optional_directory> in arguments:
# python manage.py makeapp <app_name> <optional_directory>
# Example:
# python manage.py makeapp myapp
# python manage.py makeapp myapp /path/to/directory
