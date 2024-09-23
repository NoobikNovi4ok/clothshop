from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
)
from users.models import User
from django import forms


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["login", "password"]


class UserRegistrationForm(UserCreationForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=6)
    password_repeat = forms.CharField(widget=forms.PasswordInput)
    rules = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = [
            "name",
            "surname",
            "patronymic",
            "login",
            "email",
            "password",
            "password_repeat",
            "rules",
        ]
