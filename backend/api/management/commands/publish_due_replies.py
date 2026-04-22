from django.core.management.base import BaseCommand

from api import tasks


class Command(BaseCommand):
    help = "Publish due replies for active users"

    def handle(self, *args, **options):
        posted = tasks.publish_due_replies()
        self.stdout.write(self.style.SUCCESS(f"posted_replies={posted}"))
