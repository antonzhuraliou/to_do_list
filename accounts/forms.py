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

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
                "id": "username",
                "name": "username",
                "placeholder": "Введите username",
                "required": True,
            }
        ),
    )
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
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "id": "password",
                "name": "password",
                "placeholder": "Введите password",
                "required": True,
            }
        ),
    )
    password2 = forms.CharField(
        label="Repeat password",
        widget=forms.PasswordInput(
            attrs={
                "id": "repeat password",
                "name": "repeat password",
                "placeholder": "Введите password",
                "required": True,
            }
        ),
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']