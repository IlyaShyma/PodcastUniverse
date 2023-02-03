from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
from audio_validator.validator import AudioValidator

from profileManagementApp.models import UserProfile


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Podcast(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=400)
    creation_date = models.DateField(auto_now_add=True, blank=True)
    cover = models.ImageField(upload_to="podcast_cover/")

    subscribers = models.ManyToManyField(UserProfile, related_name="subcriptions", blank=True)
    host = models.ManyToManyField(UserProfile, related_name="user_profiles", blank=True)

    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.title

class Episode(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    creation_date = models.DateField(auto_now_add=True, blank=True)
    audio = models.FileField(upload_to="audio_files/", null=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)

    favourite_episodes = models.ManyToManyField(UserProfile, related_name="liked_episode", blank=True)
    guest = models.ManyToManyField(UserProfile, blank=True)
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)

    def __str__(self):
        return self.title



class Comment(models.Model):
    creation_date = models.DateField(auto_now_add=True, blank=True)
    content = models.CharField(max_length=1000)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    reports = models.IntegerField(default=0)

    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


class Invitation(models.Model):
    CHOICES = [
        (0, "unconfirmed"),
        (1, "confirmed"),
        (2, "rejected"),
    ]

    from_user_profile = models.ForeignKey(UserProfile, blank=True, on_delete=models.CASCADE, related_name="sender", null=True)
    to_user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="receiver", null=True)
    status = models.PositiveSmallIntegerField(choices=CHOICES, default=0)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, blank=True, null=True)

