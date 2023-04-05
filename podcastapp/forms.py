from django import forms
from django.forms import Textarea

from profileManagementApp.models import UserProfile
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

# import magic

class AdvancedUserCreationFrom(forms.ModelForm):
    # helper = FormHelper()
    # helper.form_id = "complete_registration_crispy_form"
    # helper.form_method = "POST"
    # helper.add_input(Submit("submit", "Aggiungi avatar"))

    class Meta:
        model = UserProfile
        fields = ["avatar"]


class EpisodeForm(forms.ModelForm):
    class Meta:
        model = Episode
        fields = [
            "title",
            "description",
            "audio"
        ]

    def clean_audio(self):
        audio = self.cleaned_data["audio"]


        # print(magic.from_file(audio))
        # SAVE TO TEMP CHECK IF IT S VALID DELETE FROM TEMP

        return audio


class RateEpisodeForm(forms.Form):
    rate_episode = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class DeleteEpisodeForm(forms.Form):
    delete_episode_flag = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class ReportCommentForm(forms.Form):
    report_comment_flag = forms.BooleanField(widget=forms.HiddenInput,initial=True)


class CommentForm(forms.ModelForm):
    comment_flag = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = Comment
        fields = [
            "content",
        ]
        widgets = {
             "content": Textarea(attrs={"rows": 4, "cols": 70}),
        }
        exclude = ('episode', 'user_profile',)


class ChooseGuestFrom(forms.ModelForm):
    guest_flag = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = Invitation
        fields = [
            "to_user_profile"
        ]


class CreatePodcastForm(forms.ModelForm):
    class Meta:
        model = Podcast
        fields = ["title", "description", "cover", "categories"]
        labels = {
            "categories": "Choose category"
        }
