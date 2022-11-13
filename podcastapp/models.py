from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage


podcast_stor_loc = FileSystemStorage(location="/media/podcast_cover")
user_avatar_loc = FileSystemStorage(location="/media/avatar_pic")


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


# def user_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#     return 'user_{0}/{1}'.format(instance.user.id, filename)
#

class Podcast(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=400)
    creation_date = models.DateField(default=None)
    # cover = models.ImageField(storage=podcast_stor_loc)
    cover = models.ImageField(upload_to="podcast_cover/")
    categories = models.ManyToManyField(Category)


class Episode(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    creation_date = models.DateField(default=None)
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)


class UserProfile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    banned = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to="avatar_pic/")
    subscriptions = models.ManyToManyField(Podcast, blank=True)


