from django.contrib.auth import logout, authenticate, login

from django.shortcuts import render, redirect
from django.urls import reverse


from profileManagementApp.models import UserProfile
from .forms import *
from django.views.generic.edit import CreateView



def startpage(request):
    context = {}
    # if request.method == "POST":
    #     form = ChooseCategoryForm(request.POST)
    #
    # form = ChooseCategoryForm()
    # context["form"] = form
    podcasts = Podcast.objects.all().order_by("-creation_date")

    context["podcasts"] = podcasts
    if request.user.is_anonymous:
        return render(request, template_name="homepage.html", context=context)
    else:
        user_profile = UserProfile.objects.get(user=request.user.pk)
        context["user_profile"] = user_profile
        return render(request, template_name="homepage.html", context=context)


class UserCreateView(CreateView):
    form_class = CreateRegularUser
    template_name = "user_create.html"

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