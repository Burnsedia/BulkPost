from django.core.management.base import BaseCommand

from api import tasks


class Command(BaseCommand):
    help = "Publish due tweets for active users"

    def handle(self, *args, **options):
        posted = tasks.publish_due_posts()
        self.stdout.write(self.style.SUCCESS(f"posted_tweets={posted}"))
