# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SystemPromptView,
    PromptView,
    PostView,
    TweetPreviewView,
    RunPostNowView,
)

# Use DRF router for the main models
router = DefaultRouter()
router.register(r'system-prompts', SystemPromptView, basename='system-prompt')
router.register(r'prompts', PromptView, basename='prompt')
router.register(r'posts', PostView, basename='post')

urlpatterns = [
    # Core CRUD API routes
    path('', include(router.urls)),

    # Custom endpoints
    path('tweet/preview/', TweetPreviewView.as_view(), name='tweet-preview'),
    path('posts/<int:pk>/run_now/', RunPostNowView.as_view(), name='run-post-now'),
]
