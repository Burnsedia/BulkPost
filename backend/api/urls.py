# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SystemPromptView,
    PromptView,
    PostView,
)

# Use DRF router for the main models
router = DefaultRouter()
router.register(r'system-prompts', SystemPromptView, basename='system-prompt')
router.register(r'prompts', PromptView, basename='prompt')
router.register(r'posts', PostView, basename='post')

urlpatterns = [
    # Core CRUD API routes
    path('', include(router.urls)),
]
