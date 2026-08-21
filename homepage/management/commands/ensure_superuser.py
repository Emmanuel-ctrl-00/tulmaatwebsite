import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Creates an admin superuser from environment variables if one doesn't
    already exist. Safe to run on every deploy/startup — it does nothing
    if a superuser is already present, so it won't reset your password
    or duplicate accounts.

    Reads:
      DJANGO_SUPERUSER_USERNAME
      DJANGO_SUPERUSER_EMAIL
      DJANGO_SUPERUSER_PASSWORD

    Usage:
      python manage.py ensure_superuser
    """

    help = "Creates the admin superuser from env vars if none exists yet."

    def handle(self, *args, **options):
        User = get_user_model()

        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.SUCCESS("A superuser already exists — nothing to do."))
            return

        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not username or not password:
            self.stdout.write(self.style.WARNING(
                "No superuser exists, and DJANGO_SUPERUSER_USERNAME / "
                "DJANGO_SUPERUSER_PASSWORD env vars are not set — skipping. "
                "Set them (in Render's Environment tab, or your local .env) "
                "and run this command again, or use "
                "'python manage.py createsuperuser' interactively instead."
            ))
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created."))
