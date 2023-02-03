from django import forms

from podcastapp.models import Invitation
from .models import *


class InvitationApproveForm(forms.Form):
    invitation_flag = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class FollowUnfollowForm(forms.Form):
    follow_unfollow_flag = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class DeleteCommentBlockUserForm(forms.Form):
    delete_ban_flag = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class UnblockUserForm(forms.Form):
    unblock_user_flag = forms.BooleanField(widget=forms.HiddenInput, initial=True)