# views.py
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import SystemPrompt, Prompt, Post
from .serializers import SystemPromptSerializer, PromptSerializer, PostSerializer
from .services import run_post_generation_and_publish

class SystemPromptView(ModelViewSet):
    serializer_class = SystemPromptSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return SystemPrompt.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PromptView(ModelViewSet):
    serializer_class = PromptSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Prompt.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostView(ModelViewSet):  # <- switch to ModelViewSet so you can create/schedule
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).select_related("system_prompt","prompt")
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def run_now(self, request, pk=None):
        post = self.get_object()
        if post.status not in ("pending", "failed"):
            return Response({"detail":"Post already sent."}, status=status.HTTP_400_BAD_REQUEST)
        post = run_post_generation_and_publish(post)
        return Response(PostSerializer(post).data)

