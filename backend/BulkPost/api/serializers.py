from rest_framework.serializers import ModelSerializer
from .models import SystemPrompt, Prompt, Post

class SystemPromptSerializer(ModelSerializer):
    class Meta:
        model = SystemPrompt
        fields = "__all__"

class PromptSerializer(ModelSerializer):
    class Meta:
        model = Prompt
        fields = "__all__"

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
