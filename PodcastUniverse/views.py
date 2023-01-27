from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import UserCreationForm

from profileManagementApp.models import UserProfile
from podcastapp.models import Podcast
from .forms import *
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin


def startpage(request):
    podcasts = Podcast.objects.all().order_by("-creation_date")
    if request.user.is_anonymous:
        return render(request, template_name="homepage.html", context={"podcasts": podcasts})
    else:
        user_profile = UserProfile.objects.get(user=request.user.pk)
        return render(request, template_name="homepage.html", context={"user_profile": user_profile, "podcasts": podcasts})


# @login_required
# def login_next_step(request):
#     return render(request, template_name="registration_next_step.html")


# def esempio(request):
#     return render(request, template_name="fake_registration.html")


class UserCreateView(CreateView):
    form_class = CreateRegularUser
    template_name = "user_create.html"
    # success_url = reverse_lazy("registration2")
    # success_url = reverse_lazy("profileManagementApp:user_settings")

    def form_valid(self, form_class):
        to_return = super().form_valid(form_class)
        user = authenticate(
            username=form_class.cleaned_data["username"],
            password=form_class.cleaned_data["password1"],
        )
        login(self.request, user)
        return to_return

    def get_success_url(self, **kwargs):
        # obj = form.instance or self.object
        user_profile_id = UserProfile.objects.get(user=self.object.pk).pk
        return reverse("profileManagementApp:user_settings", kwargs={'pk': user_profile_id})

def user_logged_in(request):
    if request.user.is_authenticated == True:
        username = request.user.username
    else:
        username = None
    return username


def logout_view(request):
    username = user_logged_in(request)
    if username is not None:
        logout(request)
        return redirect("home")