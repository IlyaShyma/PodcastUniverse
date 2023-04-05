import django.db.models.query
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from podcastapp.forms import AdvancedUserCreationFrom, EpisodeForm, RateEpisodeForm, CommentForm, ChooseGuestFrom, \
    CreatePodcastForm, DeleteEpisodeForm, ReportCommentForm
from podcastapp.models import Podcast, Episode, Comment
from profileManagementApp.models import UserProfile
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta


class UserPodcasts(LoginRequiredMixin, ListView):
    template_name = "podcastapp/list_podcasts.html"

    def get_queryset(self):
        creator = UserProfile.objects.get(user_id=self.request.user)
        return Podcast.objects.filter(host=creator)


class CreatePodcast(LoginRequiredMixin, CreateView):
    model = Podcast
    # fields = ["title", "description", "cover", "categories"]
    form_class = CreatePodcastForm
    template_name = "podcastapp/podcast-creation.html"

    def form_valid(self, form):
        to_return = super(CreatePodcast, self).form_valid(form)
        creator = UserProfile.objects.get(user_id=self.request.user)
        form.instance.host.add(creator)
        return to_return

    success_url = reverse_lazy("podcastapp:my_podcasts")


class SubscriptionsPodcastView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = UserProfile
    template_name = "podcastapp/subscriptions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["podcasts"] = Podcast.objects.filter(subscribers=self.object)
        return context

    def test_func(self):
        obj = self.get_object().user_id
        return obj == self.request.user.id


class SubscriptionEpisodePodcastView(SubscriptionsPodcastView):
    template_name = "podcastapp/subscriptions-episodes.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        episodes_to_show = Episode.objects.none()
        for podcast in context["podcasts"]:
            episodes_to_show |= Episode.objects.filter(podcast=podcast)
        not_older_then = 10
        context["episodes"] = episodes_to_show.filter(
            creation_date__gte=datetime.now() - timedelta(not_older_then)).order_by("-creation_date")
        return context

class SubscriptionsPeopleView(SubscriptionsPodcastView):
    template_name = "podcastapp/subsriptions-users.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        me = UserProfile.objects.get(user=self.request.user)
        people_i_follow = me.following.all()

        episodes_to_show = Episode.objects.none()
        for user in people_i_follow:
            episodes_to_show |= Episode.objects.filter(guest=user)

        not_older_then = 10
        context["episodes"] = episodes_to_show.filter(
            creation_date__gte=datetime.now() - timedelta(not_older_then)).order_by("-creation_date")
        return context

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

        context["form"] = form
        context["podcast"] = podcast

        return render(request, template_name="podcastapp/add-new-episode.html", context=context)
    else:
        raise PermissionDenied


# class PodcastEpisodes(DetailView):
#     model = Podcast
#     template_name = "podcastapp/list_episodes.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         context["episodes"] = Episode.objects.filter(podcast=self.object).order_by("-creation_date")
#
#         context["creator"] = False
#         creators = self.object.host.all()
#
#
#         me = UserProfile.objects.get(user_id=self.request.user)
#         if me in creators:
#             context["creator"] = True
#         context["hosts"] = creators
#         return context


def podcast_view(request, podcast_id):
    context = {}
    podcast = get_object_or_404(Podcast, pk=podcast_id)

    context["object"] = podcast
    context["episodes"] = Episode.objects.filter(podcast=podcast).order_by("-creation_date")
    context["creator"] = False

    creators = podcast.host.all()
    subscribed = False
    me = None

    if request.user.is_authenticated:
        me = UserProfile.objects.get(user_id=request.user)

        if me in creators:
            context["creator"] = True

        if podcast in me.subcriptions.all():
            subscribed = True

    context["hosts"] = creators

    context["subscribed"] = subscribed

    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))

        if not (me in creators):
            action = request.POST.get("action")
            if action == "subscribe":
                podcast.subscribers.add(me)
            elif action == "unsubscribe":
                podcast.subscribers.remove(me)
        return HttpResponseRedirect(request.path_info)

    context["comment_form"] = CommentForm()
    return render(request, "podcastapp/list_episodes.html", context=context)


def episode_view(request, episode_id):
    episode = get_object_or_404(Episode, pk=episode_id)
    comments = Comment.objects.filter(episode=episode).order_by("-creation_date")
    me = None
    if request.user.is_authenticated:
        me = UserProfile.objects.get(user_id=request.user)

    context = {}
    session_key = "viewed_" + str(episode.title)
    comment_form = CommentForm()

    if not request.session.get(session_key, False):
        episode.view_count += 1
        episode.save()
        request.session[session_key] = True

    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))

        if "rate_episode" in request.POST:
            session_key = "rated_" + str(episode.title)
            if not request.session.get(session_key, False):
                action = request.POST.get("vote")
                if action == "like":
                    episode.likes += 1
                    episode.favourite_episodes.add(me)
                elif action == "dislike":
                    episode.dislikes += 1
                episode.save()
                request.session[session_key] = True

        if "report_comment_flag" in request.POST:

            reported_comment = get_object_or_404(Comment, pk=int(request.POST.get("report")))
            session_key = "report_" + str(reported_comment)

            if not request.session.get(session_key, False):
                reported_comment.reports += 1
                reported_comment.save()
                request.session[session_key] = True

        if "comment_flag" in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                if me.banned:
                    form.add_error("content", "You can't use page comments right now because you've been banned")
                    comment_form = form
                else:
                    form.instance.episode = episode
                    form.instance.user_profile = me
                    form.save()
                    return HttpResponseRedirect(request.path_info)


        if "guest_flag" in request.POST:
            form = ChooseGuestFrom(request.POST)
            if form.is_valid():
                form.instance.from_user_profile = me
                form.instance.episode = episode
                form.save()
                return HttpResponseRedirect(request.path_info)

        if "delete_episode_flag" in request.POST:
            podcast_id = episode.podcast.id
            Episode.objects.get(id=episode.id).delete()
            url = reverse("podcastapp:podcast_episodes", kwargs={"podcast_id": podcast_id})
            return HttpResponseRedirect(url)


        # if "user_search_flag" in request.POST:
        #     searched = request.POST.get("searched")
        #     User = get_user_model()
        #     users = User.objects.filter(username__contains=searched)
        #     return render(request, "podcastapp/search-guest.html", context)


    rate_episode_form = RateEpisodeForm()
    choose_guest_form = ChooseGuestFrom()
    delete_episode_form = DeleteEpisodeForm()
    report_comment_form = ReportCommentForm()

    context["user_profile"] = me
    context["episode"] = episode
    context["comments"] = comments
    context["rate_episode_form"] = rate_episode_form
    context["comment_form"] = comment_form
    context["report_comment_form"] = report_comment_form
    context["choose_guest_form"] = choose_guest_form
    context["delete_episode_form"] = delete_episode_form
    context["am_i_creator"] = False

    hosts = episode.podcast.host.all()
    guests = episode.guest.all()

    context["hosts"] = hosts
    context["guests"] = guests

    context["ho_aggiunto_qualcosa"] = False

    if me in hosts:
        context["am_i_creator"] = True
    return render(request, "podcastapp/episopagee.html", context=context)


def search_all(request):
    context = {}
    # context["me"] = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        searched = request.POST.get("searched")
        User = get_user_model()
        users = User.objects.filter(username__contains=searched)

        context["podcasts"] = Podcast.objects.filter(title__contains=searched)
        context["episodes"] = Episode.objects.filter(title__contains=searched)
        context["user_profiles"] = UserProfile.objects.filter(user__in=users)

        context["searched"] = searched
        print(context["episodes"])

    return render(request, "podcastapp/search-page.html", context)
