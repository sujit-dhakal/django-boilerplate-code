from django.core.management.base import BaseCommand, CommandError
from django.core.management.commands.startapp import Command as OriginalStartApp


class Command(BaseCommand):
    help = "Restricts creation of app in default structure"

    def add_arguments(self, parser):
        # Add Django's original arguments (includes name, directory, extensions, etc.)
        OriginalStartApp.add_arguments(self, parser)

        # Add ONLY the extra argument we need
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force use of Django's default startapp command",
        )

    def handle(self, *args, **options):
        if options.get("force"):
            original_command = OriginalStartApp()
            original_command.stdout = self.stdout
            original_command.stderr = self.stderr
            original_command.style = self.style
            return original_command.handle(*args, **options)

        app_name = options["name"]

        raise CommandError(
            f"❌ Use 'python manage.py makeapp {app_name}' instead!\n\n"
            "This command uses a custom app structure. "
            f"To use Django's default structure, run:\n"
            f"python manage.py startapp {app_name} --force"
        )
