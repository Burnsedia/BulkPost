from django.core.management.base import BaseCommand

from api import tasks


class Command(BaseCommand):
    help = "Generate scheduled reply drafts for active users"

    def handle(self, *args, **options):
        created = tasks.generate_replies()
        self.stdout.write(self.style.SUCCESS(f"generated_replies={created}"))
