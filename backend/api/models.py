from django.conf import settings
from django.db import models
from django.utils import choices, timezone

class PlatformChoice(models.TextChoices):
    TWITTER = "twitter", "Twitter"
    LINKEDIN = "linkedin", "LinkedIn"
    THREADS = "threads", "Threads"


class Category(models.Model):
    title = models.CharField()
    slug = models.SlugField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children"
    )

class Post(models.Model):
    title = models.CharField()
    slug = models.SlugField()
    content = models.TextField()
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="PostCategory"
    )

class PostStatus(models.Model):
    title = models.CharField()

class Schedlutle(models.Model):
    schedulted_time = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="SchedlutledPost"
    )

class TwitterPost(models.Model):
    twitterID = models.CharField(max_length=50)
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="SchedlutledPost"
    )

class LinkedInPostPost(models.Model):
    linkedinID = models.CharField(max_length=50)
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="SchedlutledPost"
    )

class ThreadsPostPost(models.Model):
    threadsID = models.CharField(max_length=50)
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="SchedlutledPost"
    )

#TODO: create text choice models or a plateform model
class Contact(models.Models):
    username = models.CharField(max_length=50)
    platform = models.CharField(max_length=50,choices=PlatformChoice.choices default=PlatformChoice.TWITTER)
    bio = models.TextField()

class LeadStatus(models.Models):
    title = models.CharField(max_length=50)

class Lead(models.Models):
    status = models.ForeignKey(
        LeadStatus,
        null=True,
        blank=True,
        related_name="LeadStutus"
    )
    contact =  models.ForeignKey(
        Contact, 
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="contacts"
    )

