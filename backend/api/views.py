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
   # permission_classes = [IsAuthenticated]
    queryset = SystemPrompt.objects.all()
   
class PromptView(ModelViewSet):
    serializer_class = PromptSerializer
   # permission_classes = [IsAuthenticated]
    queryset = Prompt.objects.all()

class PostView(ModelViewSet):  # allows create/schedule + list
    serializer_class = PostSerializer
   # permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
