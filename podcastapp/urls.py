from django.urls import path
from . import views
from .views import UserPodcasts, CreatePodcast, create_episode, episode_view, podcast_view, SubscriptionsPodcastView, SubscriptionEpisodePodcastView, search_all

app_name = "podcastapp"

urlpatterns = [
    path("mypodcasts/", UserPodcasts.as_view(), name="my_podcasts"),
    path("podcast-creation/", CreatePodcast.as_view(), name="create_podcast"),
    # path("<pk>/podcast/", PodcastEpisodes.as_view(), name="podcast_episodes"),
    path("<podcast_id>/podcast/", podcast_view, name="podcast_episodes"),
    path("<podcast_id>/add-new-episode", create_episode, name="create-episode"),
    path("<episode_id>/episode/", episode_view, name="episode-page"),
    path("<pk>/subscriptions/", SubscriptionsPodcastView.as_view(), name="subscriptions"),
    path("<pk>/subscriptions-episodes/", SubscriptionEpisodePodcastView.as_view(), name="subscriptions-episodes"),
    path("search-page/", search_all, name="search-page"),

]