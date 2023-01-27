from django import forms

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