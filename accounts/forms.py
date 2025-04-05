from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.TextInput(
            attrs={
                "id": "email",
                "name": "email",
                "placeholder": "Введите email",
                "required": True,
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "id": "password",
                "name": "password",
                "placeholder": "Введите пароль",
                "required": True,
            }
        ),
    )

