from django.conf import settings
from django.db import models
from django.utils import timezone

class Category(models.TextChoices):
    VALUE = "value", "Value"
    ENGAGEMENT = "engagement", "Engagement"
    AUTHORITY = "authority", "Authority"
    CONTRAST = "contrast", "Contrast"
    TRANSFORMATION = "transformation", "Transformation"


class QueueStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    POSTED = "posted", "Posted"
    FAILED = "failed", "Failed"
    SKIPPED = "skipped", "Skipped"


class GrowthMode(models.TextChoices):
    BALANCED = "balanced", "Balanced"
    AGGRESSIVE = "aggressive", "Aggressive"
    MAX_GROWTH = "max_growth", "Max Growth"


class TargetStatus(models.TextChoices):
    NEW = "new", "New"
    QUEUED = "queued", "Queued"
    REPLIED = "replied", "Replied"
    DISMISSED = "dismissed", "Dismissed"


class SystemPrompt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="default")
    content = models.TextField()
    model_name = models.CharField(max_length=128, default="openai:gpt-4.1-mini")
    temperature = models.FloatField(default=0.7)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}::{self.name}"


class Prompt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    category = models.CharField(max_length=50, blank=True, choices=Category.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]


class GrowthPolicy(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mode = models.CharField(
        max_length=20, choices=GrowthMode.choices, default=GrowthMode.BALANCED
    )
    timezone = models.CharField(max_length=64, default="UTC")
    target_tweets_per_day = models.PositiveIntegerField(default=5)
    target_replies_per_day = models.PositiveIntegerField(default=20)
    min_post_interval_minutes = models.PositiveIntegerField(default=90)
    min_reply_interval_seconds = models.PositiveIntegerField(default=180)
    auto_post_enabled = models.BooleanField(default=True)
    review_high_risk_only = models.BooleanField(default=True)
    relevance_threshold = models.FloatField(default=75.0)
    kill_switch = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"policy::{self.user}::{self.mode}"


class DailyUsage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.localdate)
    tweets_posted = models.PositiveIntegerField(default=0)
    replies_posted = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "date"], name="uniq_daily_usage_user_date"
            )
        ]

    def __str__(self):
        return f"usage::{self.user}::{self.date}"


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    system_prompt = models.ForeignKey(
        SystemPrompt, on_delete=models.PROTECT, null=True, blank=True
    )
    prompt = models.ForeignKey(Prompt, on_delete=models.PROTECT, null=True, blank=True)
    scheduled_for = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=16, default=QueueStatus.PENDING, choices=QueueStatus.choices
    )
    text = models.TextField(blank=True)
    twitter_id = models.CharField(max_length=64, blank=True)
    risk_score = models.FloatField(default=0.0)
    relevance_score = models.FloatField(default=0.0)
    run_reason = models.CharField(max_length=100, default="daily_autopilot")
    created_at = models.DateTimeField(auto_now_add=True)
    posted_at = models.DateTimeField(null=True, blank=True)
    error = models.TextField(blank=True, default="")

    def __str__(self):
        preview = self.text[:40] if self.text else "draft"
        return f"tweet::{self.user}::{preview}"

    class Meta:
        indexes = [
            models.Index(fields=["status", "scheduled_for"]),
            models.Index(fields=["user", "created_at"]),
            models.Index(fields=["user", "status", "scheduled_for"]),
        ]


class ReplyTarget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    source_tweet_id = models.CharField(max_length=64)
    source_author_handle = models.CharField(max_length=64)
    source_text = models.TextField()
    relevance_score = models.FloatField(default=0.0)
    status = models.CharField(
        max_length=16, default=TargetStatus.NEW, choices=TargetStatus.choices
    )
    discovered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "source_tweet_id"], name="uniq_reply_target_user_tweet"
            )
        ]
        indexes = [models.Index(fields=["user", "status", "relevance_score"])]

    def __str__(self):
        return f"target::{self.user}::{self.source_tweet_id}"


class Reply(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    target = models.ForeignKey(
        ReplyTarget, on_delete=models.PROTECT, related_name="replies"
    )
    scheduled_for = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=16, default=QueueStatus.PENDING, choices=QueueStatus.choices
    )
    text = models.TextField()
    twitter_id = models.CharField(max_length=64, blank=True)
    risk_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    posted_at = models.DateTimeField(null=True, blank=True)
    error = models.TextField(blank=True, default="")

    class Meta:
        indexes = [
            models.Index(fields=["status", "scheduled_for"]),
            models.Index(fields=["user", "status", "scheduled_for"]),
        ]

    def __str__(self):
        return f"reply::{self.user}::{self.target.source_tweet_id}"


class PostMetricSnapshot(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="metric_snapshots"
    )
    captured_at = models.DateTimeField(default=timezone.now)
    impressions = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    replies = models.PositiveIntegerField(default=0)
    reposts = models.PositiveIntegerField(default=0)
    profile_visits = models.PositiveIntegerField(default=0)
    follows = models.PositiveIntegerField(default=0)

    class Meta:
        indexes = [models.Index(fields=["captured_at"])]


class AgentRunLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    agent_name = models.CharField(max_length=100)
    action = models.CharField(max_length=100)
    success = models.BooleanField(default=True)
    detail = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["user", "created_at"])]
