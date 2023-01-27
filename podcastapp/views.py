from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from podcastapp.forms import AdvancedUserCreationFrom, EpisodeForm
from podcastapp.models import Podcast, Episode
from profileManagementApp.models import UserProfile
from django.core.exceptions import PermissionDenied


class UserPodcasts(LoginRequiredMixin, ListView):
    template_name = "podcastapp/list_podcasts.html"

    def get_queryset(self):
        creator = UserProfile.objects.get(user_id=self.request.user)
        return Podcast.objects.filter(host=creator)

class CreatePodcast(LoginRequiredMixin, CreateView):
    model = Podcast
    fields = ["title", "description", "cover"]
    template_name = "podcastapp/podcast-creation.html"

    def form_valid(self, form):
        to_return = super(CreatePodcast, self).form_valid(form)
        creator = UserProfile.objects.get(user_id=self.request.user)
        form.instance.host.add(creator)
        return to_return

    success_url = reverse_lazy("podcastapp:my_podcasts")


def create_episode(request, podcast_id):
    podcast = get_object_or_404(Podcast, pk=podcast_id)
    me = UserProfile.objects.get(user_id=request.user)
    creators = podcast.host.all()

    context = {}
    if me in creators:
        form = EpisodeForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.podcast = podcast
            form.save()
            return redirect("home")
        else:
            pass
        context["form"] = form
        context["podcast"] = podcast

        return render(request, template_name="podcastapp/add-new-episode.html", context=context)
    else:
        raise PermissionDenied

class PodcastEpisodes(LoginRequiredMixin, DetailView):
    model = Podcast
    template_name = "podcastapp/list_episodes.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["episodes"] = Episode.objects.filter(podcast=self.object)

        context["creator"] = False
        creators = self.object.host.all()
        me = UserProfile.objects.get(user_id=self.request.user)

        if me in creators:
            context["creator"] = True

        return context

class EpisodeView(LoginRequiredMixin, DetailView):
    model = Episode
    template_name = "podcastapp/episode_page.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_profile"] = UserProfile.objects.get(user_id=self.request.user)
        return context

