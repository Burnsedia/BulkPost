from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import SystemPrompt, Prompt, Post
from .serializers import SystemPromptSerializer, PromptSerializer, PostSerializer

# Create your views here
class SystemPromptView(ModelViewSet):
    serializer_class = SystemPromptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SystemPrompt.objects.filter(user=self.request.user)

class PromptView(ModelViewSet):
    serializer_class = PromptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Prompt.objects.filter(user=self.request.user)


class PostView(ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

