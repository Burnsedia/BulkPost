from rest_framework.serializers import ModelSerializer

from .models import (
    DailyUsage,
    GrowthPolicy,
    Post,
    Prompt,
    Reply,
    ReplyTarget,
    SystemPrompt,
)


class SystemPromptSerializer(ModelSerializer):
    class Meta:
        model = SystemPrompt
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at"]


class PromptSerializer(ModelSerializer):
    class Meta:
        model = Prompt
        fields = "__all__"
        read_only_fields = ["user", "created_at"]


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = [
            "user",
            "status",
            "text",
            "twitter_id",
            "created_at",
            "posted_at",
            "error",
        ]


class GrowthPolicySerializer(ModelSerializer):
    class Meta:
        model = GrowthPolicy
        fields = "__all__"
        read_only_fields = ["user", "updated_at"]


class ReplyTargetSerializer(ModelSerializer):
    class Meta:
        model = ReplyTarget
        fields = "__all__"
        read_only_fields = ["user", "discovered_at", "status"]


class ReplySerializer(ModelSerializer):
    class Meta:
        model = Reply
        fields = "__all__"
        read_only_fields = [
            "user",
            "status",
            "twitter_id",
            "created_at",
            "posted_at",
            "error",
        ]


class DailyUsageSerializer(ModelSerializer):
    class Meta:
        model = DailyUsage
        fields = "__all__"
