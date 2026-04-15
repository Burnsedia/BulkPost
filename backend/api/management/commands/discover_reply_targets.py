from django.core.management.base import BaseCommand

from api import tasks


class Command(BaseCommand):
    help = "Discover reply targets from X search"

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit", type=int, default=100, help="Maximum targets per user"
        )

    def handle(self, *args, **options):
        created = tasks.discover_reply_targets(limit_per_user=options["limit"])
        self.stdout.write(self.style.SUCCESS(f"created_reply_targets={created}"))
