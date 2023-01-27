from django.urls import path
from .views import *

app_name = "profileManagementApp"

urlpatterns = [
    # path("<int:pk>/settings/", user_settings, name="user_settings")
    path("<int:pk>/settings/", UserUpdateView.as_view(), name="user_settings")
]