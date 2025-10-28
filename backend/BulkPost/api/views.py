from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .models import SystemPrompt, Prompt, Post
from .serializers import Sy



# Create your views here
class SystemPromptView(ModelViewSet):
    pass

class PromptView(ModelViewSet):
    pass

class PostView(ReadOnlyModelViewSet):
    pass
