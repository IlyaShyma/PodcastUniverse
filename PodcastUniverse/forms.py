from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

class CreateRegularUser(UserCreationForm):
    def save(self, commit=True):
        user = super().save(commit)
        g = Group.objects.get(name="regular_user")
        g.user_set.add(user)
        return user