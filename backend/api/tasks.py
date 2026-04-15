from __future__ import annotations

from . import services


def generate_daily_posts() -> int:
    total = 0
    for user in services.active_users():
        total += services.generate_daily_posts_for_user(user)
    return total


def publish_due_posts() -> int:
    total = 0
    for user in services.active_users():
        total += services.publish_due_posts_for_user(user)
    return total


def discover_reply_targets(limit_per_user: int = 100) -> int:
    total = 0
    for user in services.active_users():
        total += services.discover_reply_targets_for_user(user, limit=limit_per_user)
    return total


def generate_replies() -> int:
    total = 0
    for user in services.active_users():
        total += services.generate_replies_for_user(user)
    return total


def publish_due_replies() -> int:
    total = 0
    for user in services.active_users():
        total += services.publish_due_replies_for_user(user)
    return total


def collect_metrics() -> int:
    total = 0
    for user in services.active_users():
        total += services.collect_metrics_for_user(user)
    return total


def daily_reset_counters() -> int:
    return services.reset_daily_usage()
