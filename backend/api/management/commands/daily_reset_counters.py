from django.core.management.base import BaseCommand

from api import tasks


class Command(BaseCommand):
    help = "Reset daily usage counters"

    def handle(self, *args, **options):
        updated = tasks.daily_reset_counters()
        self.stdout.write(self.style.SUCCESS(f"daily_usage_reset={updated}"))
