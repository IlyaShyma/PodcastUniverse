from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db.models.signals import post_save
from django.dispatch import receiver

# from podcastapp.models import Podcast


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_bio = models.CharField(max_length=150, null=True)
    banned = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to="avatar_pic/", default="default/default_avatar.jpg")
    following = models.ManyToManyField("self", related_name="followers", blank=True, symmetrical=False)

    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=User)
def create_profile_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


