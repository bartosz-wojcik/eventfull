from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'password', 'email')


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'username')
