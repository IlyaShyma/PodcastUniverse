
from django.http import HttpResponseRedirect

from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, DetailView
from profileManagementApp.forms import InvitationApproveForm, FollowUnfollowForm, DeleteCommentBlockUserForm, UnblockUserForm
from profileManagementApp.models import UserProfile
from podcastapp.models import Comment, Podcast, Episode, Invitation
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    fields = {
        "avatar",
        "profile_bio"
    }
    template_name = "profileManagementApp/user_settings.html"

    def test_func(self):
        obj = self.get_object().user_id
        return obj == self.request.user.id

    success_url = reverse_lazy("home")


# class UserPageView(DetailView):
#     model = UserProfile
#     template_name = "profileManagementApp/user-page.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         context["comments"] = Comment.objects.filter(user_profile=self.object)
#         context["host"] = Podcast.objects.filter(host=self.object)
#         context["episodes"] = Episode.objects.filter(guest=self.object)
#
#         return context


def user_page_view(request, user_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    userprofile = get_object_or_404(UserProfile, pk=user_id)
    me = UserProfile.objects.get(user_id=request.user)
    context = {}

    following_right_now = False
    if userprofile in me.following.all():
        following_right_now = True

    if request.method == "POST":

        if "invitation_flag" in request.POST:

            if request.POST.get("true"):
                invitation = get_object_or_404(Invitation, pk=int(request.POST.get("true")))
                invitation.status = 1
                invitation.episode.guest.add(me)
                invitation.save()

            elif request.POST.get("false"):
                invitation = get_object_or_404(Invitation, pk=int(request.POST.get("false")))
                invitation.status = 2
                invitation.save()

        elif "follow_unfollow_flag" in request.POST:
            if me != userprofile:
                action = request.POST.get("follow_action")
                if action == "follow" and not following_right_now:
                    me.following.add(userprofile)
                    return HttpResponseRedirect(request.path_info)
                elif action == "unfollow" and following_right_now:
                    me.following.remove(userprofile)
                return HttpResponseRedirect(request.path_info)

    form = InvitationApproveForm()
    follow_unfollow_form = FollowUnfollowForm()

    context["form"] = form
    context["follow_unfollow_form"] = follow_unfollow_form
    context["following_right_now"] = following_right_now
    context["my_subscribers"] = me.followers.all()
    context["userprofile"] = userprofile
    context["comments"] = Comment.objects.filter(user_profile=userprofile)
    context["host"] = Podcast.objects.filter(host=userprofile)
    context["episodes"] = Episode.objects.filter(guest=userprofile).order_by("-creation_date")
    context["favourite_episodes"] = Episode.objects.filter(favourite_episodes=userprofile)

    context["invitations"] = False
    if me == userprofile:
        context["invitations"] = Invitation.objects.filter(to_user_profile=userprofile).filter(status=0)

    return render(request, "profileManagementApp/user-page.html", context=context)


def is_system_admin(user):
    return user.groups.filter(name="system_admin").exists()


@user_passes_test(is_system_admin)
def admin_page_view(request):
    context = {}
    comments = Comment.objects.all().filter(reports__gte=1).order_by("-reports")
    banned_users = UserProfile.objects.all().filter(banned=True)

    if request.method == "POST":
        if "delete_ban_flag" in request.POST:

            if request.POST.get("true"):
                comment_to_delete = get_object_or_404(Comment, pk=int(request.POST.get("true")))
                user_to_ban = comment_to_delete.user_profile
                comment_to_delete.delete()

                user_to_ban.banned = True
                user_to_ban.save()

            if request.POST.get("false"):
                comment = get_object_or_404(Comment, pk=int(request.POST.get("false")))
                comment.reports = 0
                comment.save()

        if "unblock_user_flag" in request.POST:
            if request.POST.get("true"):
                user_to_unblock = get_object_or_404(UserProfile, pk=int(request.POST.get("true")))
                user_to_unblock.banned = False
                user_to_unblock.save()

    delete_block_form = DeleteCommentBlockUserForm()
    unblock_user_form = UnblockUserForm()

    context["comments"] = comments
    context["banned_users"] = banned_users

    context["delete_block_form"] = delete_block_form
    context["unblock_user_form"] = unblock_user_form

    return render(request, "profileManagementApp/system-admin-page.html", context)
