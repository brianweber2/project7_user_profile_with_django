from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from . import models


User = get_user_model()

class UserCreateForm(UserCreationForm):
    """Form for creating a new user."""
    class Meta:
        fields = (
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )
        model = get_user_model()


class UserProfileUpdateForm(forms.ModelForm):
    """Update user profile information."""
    class Meta:
        model = models.UserProfile
        fields = ['dob', 'bio', 'avatar']


class UserUpdateForm(forms.ModelForm):
    """Form for updating user basic information."""
    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'email']
