# views.py
from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import SystemPrompt, Prompt, Post
from .serializers import SystemPromptSerializer, PromptSerializer, PostSerializer



class SystemPromptView(ModelViewSet):
    serializer_class = SystemPromptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            SystemPrompt.objects
            .filter(user=self.request.user)
            .order_by("-updated_at", "-created_at")
        )

class PromptView(ModelViewSet):
    serializer_class = PromptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        q = Prompt.objects.filter(user=self.request.user).order_by("-created_at")
        # Optional quick search by ?q=
        term = self.request.query_params.get("q")
        if term:
            q = q.filter(text__icontains=term)
        return q


class PostView(ModelViewSet):  # allows create/schedule + list
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = (
            Post.objects
            .filter(user=self.request.user)
            .select_related("system_prompt", "prompt")
            .order_by("-created_at")
        )
        status_param = self.request.query_params.get("status")
        if status_param:
            qs = qs.filter(status=status_param)
        return qs

