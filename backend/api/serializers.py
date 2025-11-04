# serializers.py
from rest_framework.serializers import ModelSerializer
from .models import SystemPrompt, Prompt, Post

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
        read_only_fields = ["user", "status", "text", "twitter_id", "created_at", "posted_at", "error"]

