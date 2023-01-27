from django.contrib.auth.decorators import login_required
from django.template.context_processors import request
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from profileManagementApp.models import UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# @login_required
# def user_settings(request):
#     return render(request, template_name="user_settings.html")

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = UserProfile
    fields = {
        "avatar"
    }
    template_name = "user_settings.html"

    def test_func(self):
        obj = self.get_object().user_id
        # print(obj)
        # print(self.request.user.id)
        return obj == self.request.user.id

    success_url = reverse_lazy("home")