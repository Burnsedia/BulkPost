from django.core.management.base import BaseCommand

from api import tasks


class Command(BaseCommand):
    help = "Collect post metric snapshots"

    def handle(self, *args, **options):
        snapshots = tasks.collect_metrics()
        self.stdout.write(self.style.SUCCESS(f"metric_snapshots={snapshots}"))
