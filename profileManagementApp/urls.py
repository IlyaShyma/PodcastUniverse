from django.urls import path
from .views import *

app_name = "profileManagementApp"

urlpatterns = [
    # path("<int:pk>/settings/", user_settings, name="user_settings")
    path("<int:pk>/settings/", UserUpdateView.as_view(), name="user_settings"),
    # path("<int:pk>/user-page/", UserPageView.as_view(), name="user-page"),
    path("<int:user_id>/user-page/", user_page_view, name="user-page"),
    path("system-admin-page/", admin_page_view, name="system-admin-page")
]