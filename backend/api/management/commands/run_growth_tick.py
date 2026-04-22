from django.core.management.base import BaseCommand

from api import tasks


class Command(BaseCommand):
    help = "Run one full growth automation tick"

    def add_arguments(self, parser):
        parser.add_argument("--discover-limit", type=int, default=100)

    def handle(self, *args, **options):
        generated_posts = tasks.generate_daily_posts()
        discovered = tasks.discover_reply_targets(
            limit_per_user=options["discover_limit"]
        )
        generated_replies = tasks.generate_replies()
        posted_tweets = tasks.publish_due_posts()
        posted_replies = tasks.publish_due_replies()
        snapshots = tasks.collect_metrics()
        self.stdout.write(
            self.style.SUCCESS(
                " ".join(
                    [
                        f"generated_posts={generated_posts}",
                        f"discovered_targets={discovered}",
                        f"generated_replies={generated_replies}",
                        f"posted_tweets={posted_tweets}",
                        f"posted_replies={posted_replies}",
                        f"snapshots={snapshots}",
                    ]
                )
            )
        )
