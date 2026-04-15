from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

from . import agents
from .models import (
    AgentRunLog,
    DailyUsage,
    GrowthMode,
    GrowthPolicy,
    Post,
    PostMetricSnapshot,
    Prompt,
    QueueStatus,
    Reply,
    ReplyTarget,
    TargetStatus,
)


User = get_user_model()


@dataclass
class PublishResult:
    success: bool
    twitter_id: str = ""
    error: str = ""


class TwitterAdapter:
    def __init__(self):
        self._client = None
        self._dry_run = os.getenv("TWITTER_DRY_RUN", "false").lower() == "true"

    def _get_client(self):
        if self._dry_run:
            return None
        if self._client is not None:
            return self._client

        try:
            import tweepy
        except Exception as exc:
            raise RuntimeError("tweepy is required for non-dry-run publishing") from exc

        self._client = tweepy.Client(
            consumer_key=os.getenv("TWITTER_API_KEY"),
            consumer_secret=os.getenv("TWITTER_API_SECRET"),
            access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
            bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
            wait_on_rate_limit=True,
        )
        return self._client

    def publish_tweet(
        self, text: str, in_reply_to_tweet_id: str | None = None
    ) -> PublishResult:
        if self._dry_run:
            fake_id = f"dryrun-{int(timezone.now().timestamp())}"
            return PublishResult(success=True, twitter_id=fake_id)

        try:
            client = self._get_client()
            resp = client.create_tweet(
                text=text, in_reply_to_tweet_id=in_reply_to_tweet_id
            )
            tweet_id = str(resp.data.get("id", "")) if resp and resp.data else ""
            return PublishResult(success=True, twitter_id=tweet_id)
        except Exception as exc:
            return PublishResult(success=False, error=str(exc))

    def discover_targets(self, keywords: list[str], limit: int = 50) -> list[dict]:
        if self._dry_run:
            return []

        client = self._get_client()
        query = " OR ".join(f"({k})" for k in keywords if k.strip())
        if not query:
            return []

        resp = client.search_recent_tweets(
            query=f"{query} -is:retweet -is:reply lang:en",
            max_results=min(limit, 100),
            tweet_fields=["author_id", "created_at"],
            expansions=["author_id"],
            user_fields=["username"],
        )
        users = (
            {u.id: u.username for u in (resp.includes or {}).get("users", [])}
            if resp.includes
            else {}
        )
        rows = []
        for tweet in resp.data or []:
            rows.append(
                {
                    "source_tweet_id": str(tweet.id),
                    "source_author_handle": users.get(tweet.author_id, "unknown"),
                    "source_text": tweet.text,
                }
            )
        return rows


def get_or_create_policy(user) -> GrowthPolicy:
    policy, _ = GrowthPolicy.objects.get_or_create(user=user)
    return policy


def usage_today(user) -> DailyUsage:
    usage, _ = DailyUsage.objects.get_or_create(user=user, date=timezone.localdate())
    return usage


def _mode_targets(mode: str) -> tuple[int, int]:
    if mode == GrowthMode.AGGRESSIVE:
        return 8, 30
    if mode == GrowthMode.MAX_GROWTH:
        return 17, 50
    return 5, 20


def apply_mode_targets(policy: GrowthPolicy) -> None:
    tweets, replies = _mode_targets(policy.mode)
    policy.target_tweets_per_day = tweets
    policy.target_replies_per_day = replies
    policy.save(
        update_fields=["target_tweets_per_day", "target_replies_per_day", "updated_at"]
    )


def _last_posted_time(user, model_cls):
    row = (
        model_cls.objects.filter(user=user, status=QueueStatus.POSTED)
        .order_by("-posted_at")
        .first()
    )
    return row.posted_at if row else None


def can_post_tweet(user, policy: GrowthPolicy) -> tuple[bool, str]:
    if policy.kill_switch:
        return False, "kill switch active"
    usage = usage_today(user)
    if usage.tweets_posted >= policy.target_tweets_per_day:
        return False, "tweet daily cap reached"
    last_posted = _last_posted_time(user, Post)
    if last_posted:
        min_next = last_posted + timedelta(minutes=policy.min_post_interval_minutes)
        if timezone.now() < min_next:
            return False, "tweet interval not met"
    return True, "ok"


def can_post_reply(user, policy: GrowthPolicy) -> tuple[bool, str]:
    if policy.kill_switch:
        return False, "kill switch active"
    usage = usage_today(user)
    if usage.replies_posted >= policy.target_replies_per_day:
        return False, "reply daily cap reached"
    last_posted = _last_posted_time(user, Reply)
    if last_posted:
        min_next = last_posted + timedelta(seconds=policy.min_reply_interval_seconds)
        if timezone.now() < min_next:
            return False, "reply interval not met"
    return True, "ok"


def _tweet_time_slots(count: int) -> list[timezone.datetime]:
    if count <= 0:
        return []
    now = timezone.now()
    day_start = now.replace(hour=8, minute=0, second=0, microsecond=0)
    day_end = now.replace(hour=23, minute=0, second=0, microsecond=0)
    if now > day_start:
        day_start = now + timedelta(minutes=5)
    total_seconds = int((day_end - day_start).total_seconds())
    if total_seconds <= 0:
        day_start = now + timedelta(minutes=5)
        day_end = day_start + timedelta(hours=8)
        total_seconds = int((day_end - day_start).total_seconds())
    step = max(total_seconds // max(count, 1), 1)
    return [day_start + timedelta(seconds=step * i) for i in range(count)]


def _reply_time_slots(count: int) -> list[timezone.datetime]:
    if count <= 0:
        return []
    now = timezone.now() + timedelta(minutes=5)
    step_seconds = max(90, int(10 * 60 * 60 / max(count, 1)))
    return [now + timedelta(seconds=step_seconds * i) for i in range(count)]


def _log(user, agent_name: str, action: str, success: bool, detail: str = "") -> None:
    AgentRunLog.objects.create(
        user=user, agent_name=agent_name, action=action, success=success, detail=detail
    )


def generate_daily_posts_for_user(user) -> int:
    policy = get_or_create_policy(user)
    apply_mode_targets(policy)
    if policy.kill_switch:
        _log(
            user,
            "agents-orchestrator",
            "generate_daily_posts",
            False,
            "kill switch active",
        )
        return 0

    pending_count = Post.objects.filter(
        user=user, status=QueueStatus.PENDING, scheduled_for__date=timezone.localdate()
    ).count()
    usage = usage_today(user)
    remaining = max(
        policy.target_tweets_per_day - (usage.tweets_posted + pending_count), 0
    )
    if remaining == 0:
        return 0

    prompts = list(Prompt.objects.filter(user=user).order_by("-created_at")[:100])
    if not prompts:
        prompts = [
            Prompt(user=user, text="Share a practical lesson from building in public.")
        ]

    slots = _tweet_time_slots(remaining)
    created = 0
    for idx, scheduled_for in enumerate(slots):
        prompt = prompts[idx % len(prompts)]
        draft = agents.generate_tweet_draft(prompt.text, seed=idx)
        status = (
            QueueStatus.APPROVED if policy.auto_post_enabled else QueueStatus.PENDING
        )
        Post.objects.create(
            user=user,
            prompt=prompt if prompt.pk else None,
            scheduled_for=scheduled_for,
            status=status,
            text=draft.text,
            risk_score=draft.risk_score,
            relevance_score=draft.relevance_score,
        )
        created += 1

    _log(user, "ai-engineer", "generate_daily_posts", True, f"created={created}")
    return created


def publish_due_posts_for_user(user, adapter: TwitterAdapter | None = None) -> int:
    adapter = adapter or TwitterAdapter()
    policy = get_or_create_policy(user)
    posted = 0

    queue = Post.objects.filter(
        user=user,
        status__in=[QueueStatus.PENDING, QueueStatus.APPROVED],
        scheduled_for__lte=timezone.now(),
    ).order_by("scheduled_for")

    for post in queue:
        allowed, reason = can_post_tweet(user, policy)
        if not allowed:
            break

        if (
            policy.review_high_risk_only
            and post.risk_score >= 0.8
            and post.status != QueueStatus.APPROVED
        ):
            post.status = QueueStatus.SKIPPED
            post.error = "high-risk content requires review"
            post.save(update_fields=["status", "error"])
            continue

        result = adapter.publish_tweet(post.text)
        if result.success:
            with transaction.atomic():
                post.status = QueueStatus.POSTED
                post.twitter_id = result.twitter_id
                post.posted_at = timezone.now()
                post.error = ""
                post.save(update_fields=["status", "twitter_id", "posted_at", "error"])
                usage = usage_today(user)
                usage.tweets_posted += 1
                usage.save(update_fields=["tweets_posted", "updated_at"])
            posted += 1
        else:
            post.status = QueueStatus.FAILED
            post.error = result.error
            post.save(update_fields=["status", "error"])

    _log(user, "agents-orchestrator", "publish_due_posts", True, f"posted={posted}")
    return posted


def discover_reply_targets_for_user(user, limit: int = 50) -> int:
    policy = get_or_create_policy(user)
    if policy.kill_switch:
        return 0

    keywords_raw = os.getenv(
        "GROWTH_KEYWORDS", "django,pydantic ai,saas,indie hacker,build in public"
    )
    keywords = [k.strip() for k in keywords_raw.split(",") if k.strip()]
    adapter = TwitterAdapter()
    rows = adapter.discover_targets(keywords=keywords, limit=limit)

    created = 0
    for row in rows:
        relevance = max(policy.relevance_threshold, 75.0)
        obj, was_created = ReplyTarget.objects.get_or_create(
            user=user,
            source_tweet_id=row["source_tweet_id"],
            defaults={
                "source_author_handle": row["source_author_handle"],
                "source_text": row["source_text"],
                "relevance_score": relevance,
            },
        )
        if was_created:
            created += 1
        elif obj.status == TargetStatus.DISMISSED:
            obj.status = TargetStatus.NEW
            obj.save(update_fields=["status"])

    _log(user, "growth-hacker", "discover_reply_targets", True, f"created={created}")
    return created


def generate_replies_for_user(user) -> int:
    policy = get_or_create_policy(user)
    if policy.kill_switch:
        return 0

    usage = usage_today(user)
    pending = Reply.objects.filter(
        user=user, status=QueueStatus.PENDING, scheduled_for__date=timezone.localdate()
    ).count()
    remaining = max(policy.target_replies_per_day - (usage.replies_posted + pending), 0)
    if remaining == 0:
        return 0

    targets = ReplyTarget.objects.filter(
        user=user,
        status=TargetStatus.NEW,
        relevance_score__gte=policy.relevance_threshold,
    ).order_by("-relevance_score", "discovered_at")[:remaining]
    slots = _reply_time_slots(len(targets))

    created = 0
    for idx, target in enumerate(targets):
        draft = agents.generate_reply_draft(target.source_text)
        Reply.objects.create(
            user=user,
            target=target,
            scheduled_for=slots[idx]
            if idx < len(slots)
            else timezone.now() + timedelta(minutes=5),
            status=QueueStatus.APPROVED
            if policy.auto_post_enabled
            else QueueStatus.PENDING,
            text=draft.text,
            risk_score=draft.risk_score,
        )
        target.status = TargetStatus.QUEUED
        target.save(update_fields=["status"])
        created += 1

    _log(user, "ai-engineer", "generate_replies", True, f"created={created}")
    return created


def publish_due_replies_for_user(user, adapter: TwitterAdapter | None = None) -> int:
    adapter = adapter or TwitterAdapter()
    policy = get_or_create_policy(user)
    posted = 0

    queue = (
        Reply.objects.filter(
            user=user,
            status__in=[QueueStatus.PENDING, QueueStatus.APPROVED],
            scheduled_for__lte=timezone.now(),
        )
        .select_related("target")
        .order_by("scheduled_for")
    )

    for reply in queue:
        allowed, reason = can_post_reply(user, policy)
        if not allowed:
            break

        if (
            policy.review_high_risk_only
            and reply.risk_score >= 0.8
            and reply.status != QueueStatus.APPROVED
        ):
            reply.status = QueueStatus.SKIPPED
            reply.error = "high-risk reply requires review"
            reply.save(update_fields=["status", "error"])
            continue

        result = adapter.publish_tweet(
            reply.text, in_reply_to_tweet_id=reply.target.source_tweet_id
        )
        if result.success:
            with transaction.atomic():
                reply.status = QueueStatus.POSTED
                reply.twitter_id = result.twitter_id
                reply.posted_at = timezone.now()
                reply.error = ""
                reply.save(update_fields=["status", "twitter_id", "posted_at", "error"])
                target = reply.target
                target.status = TargetStatus.REPLIED
                target.save(update_fields=["status"])
                usage = usage_today(user)
                usage.replies_posted += 1
                usage.save(update_fields=["replies_posted", "updated_at"])
            posted += 1
        else:
            reply.status = QueueStatus.FAILED
            reply.error = result.error
            reply.save(update_fields=["status", "error"])

    _log(user, "agents-orchestrator", "publish_due_replies", True, f"posted={posted}")
    return posted


def collect_metrics_for_user(user) -> int:
    posts = Post.objects.filter(
        user=user, status=QueueStatus.POSTED, posted_at__isnull=False
    ).order_by("-posted_at")[:100]
    created = 0
    for post in posts:
        PostMetricSnapshot.objects.create(post=post)
        created += 1

    _log(user, "analytics-reporter", "collect_metrics", True, f"snapshots={created}")
    return created


def reset_daily_usage() -> int:
    updated = DailyUsage.objects.filter(date=timezone.localdate()).update(
        tweets_posted=0, replies_posted=0
    )
    return updated


def active_users():
    return User.objects.filter(is_active=True)
