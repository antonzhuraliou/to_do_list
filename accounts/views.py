from .forms import LoginForm, RegisterForm, ChangeUsernameForm, ChangeEmailForm
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import ChangePasswordForm
from django.contrib.auth import update_session_auth_hash

def get_welcome_page(request):
    if request.user.is_authenticated:
        return redirect("tasks:main_page")
    return render(request, 'accounts/welcome_page.html')


def custom_login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            try:
                user_obj = User.objects.get(email=email)
            except User.DoesNotExist:
                form.add_error('email', 'No user found with this email.')
                return render(request, "registration/login.html", {'form': form})

            user = authenticate(request, username=user_obj.username, password=password)
            if user is not None:
                login(request, user)
                return redirect("tasks:main_page")
            else:
                form.add_error('password', 'Enter a valid password')
                return render(request, "registration/login.html", {'form': form})
    else:
        form = LoginForm()

    return render(request, "registration/login.html", {'form': form})


@login_required
def get_profile(request):
    user_email = request.user.email
    usermame = request.user.username
    return render(request, 'accounts/profile.html', context={'email':user_email, 'name': usermame})


def get_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['username']
            email = form.cleaned_data['email']
            form.save()
            send_mail(subject='Welcome! Your account has been created',message=f'Hi {user},\nThank you for registering with us! Your account has been successfully created. We are happy to have you on board!',
                      from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[email])
            return render(request, 'accounts/success_registration.html')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})

@login_required
def change_username(request, change):
    user = User.objects.get(id=request.user.id)

    if change == 'username':
        form = ChangeUsernameForm
    else:
        form = ChangeEmailForm

    if request.method == 'POST':
        form = form(request.POST, instance = user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
        else:
            return render(request, 'accounts/change_profile_info.html', context={'form':form})

    form = form(instance=user)
    return render(request, 'accounts/change_profile_info.html', context = {'form': form})


def change_password(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user)
            return redirect('accounts:profile')
        else:
            return render(request, 'registration/password_change_form.html', context = {'form': form})

    form = ChangePasswordForm(user)

    return render(request, 'registration/password_change_form.html', context = {'form': form})