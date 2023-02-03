from profileManagementApp.models import UserProfile

def user_profile_renderer(request):
    if request.user.is_authenticated:
        return {
            "me": UserProfile.objects.get(user=request.user),
        }
    else:
        return {
            "me": None,
        }

