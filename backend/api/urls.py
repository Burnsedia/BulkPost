# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DailyUsageView,
    GrowthPolicyView,
    SystemPromptView,
    ReplyTargetView,
    ReplyView,
    PromptView,
    PostView,
)

# Use DRF router for the main models
router = DefaultRouter()
router.register(r"system-prompts", SystemPromptView, basename="system-prompt")
router.register(r"prompts", PromptView, basename="prompt")
router.register(r"posts", PostView, basename="post")
router.register(r"growth-policies", GrowthPolicyView, basename="growth-policy")
router.register(r"reply-targets", ReplyTargetView, basename="reply-target")
router.register(r"replies", ReplyView, basename="reply")
router.register(r"daily-usage", DailyUsageView, basename="daily-usage")

urlpatterns = [
    # Core CRUD API routes
    path("", include(router.urls)),
]
