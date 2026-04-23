from django.conf import settings
from django.db import models
from django.utils import timezone

class Category(models.Model):
    title = models.CharField()
    slug = models.SlugField()
    description = models.TextField()
    created_at = models.Date
