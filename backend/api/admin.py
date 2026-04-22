from django.contrib import admin

from .models import (
    AgentRunLog,
    DailyUsage,
    GrowthPolicy,
    Post,
    PostMetricSnapshot,
    Prompt,
    Reply,
    ReplyTarget,
    SystemPrompt,
)


@admin.register(SystemPrompt)
class SystemPromptAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name", "model_name", "updated_at")
    search_fields = ("user__username", "name")


@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "category", "created_at")
    list_filter = ("category",)
    search_fields = ("user__username", "text")


@admin.register(GrowthPolicy)
class GrowthPolicyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "mode",
        "target_tweets_per_day",
        "target_replies_per_day",
        "auto_post_enabled",
        "kill_switch",
    )
    list_filter = ("mode", "auto_post_enabled", "kill_switch")
    search_fields = ("user__username",)


@admin.register(DailyUsage)
class DailyUsageAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "date", "tweets_posted", "replies_posted")
    list_filter = ("date",)
    search_fields = ("user__username",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "status",
        "scheduled_for",
        "posted_at",
        "risk_score",
        "relevance_score",
    )
    list_filter = ("status",)
    search_fields = ("user__username", "text", "twitter_id")


@admin.register(ReplyTarget)
class ReplyTargetAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "source_author_handle",
        "relevance_score",
        "status",
        "discovered_at",
    )
    list_filter = ("status",)
    search_fields = (
        "user__username",
        "source_author_handle",
        "source_text",
        "source_tweet_id",
    )


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "target",
        "status",
        "scheduled_for",
        "posted_at",
        "risk_score",
    )
    list_filter = ("status",)
    search_fields = ("user__username", "text", "twitter_id")


@admin.register(PostMetricSnapshot)
class PostMetricSnapshotAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "post",
        "captured_at",
        "impressions",
        "likes",
        "replies",
        "follows",
    )
    list_filter = ("captured_at",)


@admin.register(AgentRunLog)
class AgentRunLogAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "agent_name", "action", "success", "created_at")
    list_filter = ("agent_name", "success")
    search_fields = ("user__username", "agent_name", "action", "detail")
