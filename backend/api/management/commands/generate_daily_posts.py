from django.core.management.base import BaseCommand

from api import tasks


class Command(BaseCommand):
    help = "Generate scheduled tweet drafts for active users"

    def handle(self, *args, **options):
        created = tasks.generate_daily_posts()
        self.stdout.write(self.style.SUCCESS(f"generated_posts={created}"))
