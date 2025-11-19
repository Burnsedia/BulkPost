# models.py
from django.db import models
from django.conf import settings
from django.utils import timezone

class Category(models.TextChoices):
    VALUE = "value", "Value"
    ENGAGEMENT = "engagement", "Engagement"
    AUTHORITY = "authority", "Authority"
    CONTRAST = "contrast", "Contrast"
    TRANSFORMATION = "transformation", "Transformation"

class SystemPrompt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="default")
    content = models.TextField()
    model_name = models.CharField(max_length=64, default="gpt-4o-mini")  # <- add
    temperature = models.FloatField(default=0.7)                           # <- add
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self): return f"{self.user}::{self.name}"

class Prompt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    category = models.CharField(
        max_length=50, blank=True, choices=Category.choices
    )  # optional but consistent
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.text[:50]

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    system_prompt = models.ForeignKey(SystemPrompt, on_delete=models.PROTECT)
    prompt = models.ForeignKey(Prompt, on_delete=models.PROTECT)
    scheduled_for = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=16, default="pending")  # pending|posted|failed
    text = models.TextField(blank=True)            # final composed tweet text
    twitter_id = models.CharField(max_length=64, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    posted_at = models.DateTimeField(null=True, blank=True)
    error = models.TextField(blank=True, default="")             # <- add

    def __str__(self): return f"{self.user} - {self.prompt.text[:40]}"

    class Meta:
        indexes = [
            models.Index(fields=["status", "scheduled_for"]),
            models.Index(fields=["user", "created_at"]),
        ]
