from django.urls import path
from . import views
from .views import UserPodcasts, CreatePodcast, PodcastEpisodes, create_episode, EpisodeView

app_name = "podcastapp"

urlpatterns = [
    path("mypodcasts/", UserPodcasts.as_view(), name="my_podcasts"),
    path("podcast-creation/", CreatePodcast.as_view(), name="create_podcast"),
    path("<pk>/podcast/", PodcastEpisodes.as_view(), name="podcast_episodes"),
    path("<podcast_id>/add-new-episode", create_episode, name="create-episode"),
    path("<pk>/episode/", EpisodeView.as_view(), name="episode-page"),

]