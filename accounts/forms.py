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
                "placeholder": "Enter your email",
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
                "placeholder": "Enter your password",
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
                "placeholder": "Enter your username",
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
                "placeholder": "Enter your email",
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
                "placeholder": "Enter your password",
                "required": True,
            }
        ),
    )
    password2 = forms.CharField(
        label="Repeat password",
        widget=forms.PasswordInput(
            attrs={
                "id": "repeat-password",
                "name": "repeat password",
                "placeholder": "Enter your password",
                "required": True,
            }
        ),
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('An email address must be unique.')
        return email

class ChangeUsernameForm(forms.ModelForm):

    username = forms.CharField(
        label="New name",
        widget = forms.TextInput(
            attrs={
                "id": "new-name",
                "name": "username",
                "placeholder": "Enter your new name...",
                "required": True,
            }
        ),
    )

    class Meta:
        model = User
        fields = ['username']


class ChangeEmailForm(forms.ModelForm):

    email = forms.CharField(
        label="New email",
        widget = forms.TextInput(
            attrs={
                "id": "new-email",
                "name": "email",
                "placeholder": "Enter your new email...",
                "required": True,
            }
        ),
    )

    class Meta:
        model = User
        fields = ['email']