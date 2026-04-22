from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import (
    DailyUsage,
    GrowthPolicy,
    Post,
    Prompt,
    Reply,
    ReplyTarget,
    SystemPrompt,
)
from .serializers import (
    DailyUsageSerializer,
    GrowthPolicySerializer,
    PostSerializer,
    PromptSerializer,
    ReplySerializer,
    ReplyTargetSerializer,
    SystemPromptSerializer,
)


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


class PostView(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GrowthPolicyView(ModelViewSet):
    serializer_class = GrowthPolicySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GrowthPolicy.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReplyTargetView(ModelViewSet):
    serializer_class = ReplyTargetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ReplyTarget.objects.filter(user=self.request.user)


class ReplyView(ModelViewSet):
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reply.objects.filter(user=self.request.user)


class DailyUsageView(ModelViewSet):
    serializer_class = DailyUsageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DailyUsage.objects.filter(user=self.request.user)
