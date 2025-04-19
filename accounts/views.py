from .forms import LoginForm, RegisterForm, ChangeUsernameForm, ChangeEmailForm, ContactUsForm
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import ChangePasswordForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .utils import email_messages, send_contact_email_reply, send_email_for_person


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
            email = form.cleaned_data['email']
            form.save()
            send_email_for_person(subject= email_messages['after_registration']['subject'],message= email_messages['after_registration']['message'],
                      email=email)
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
            messages.add_message(request, messages.SUCCESS, 'Your Username Has Been Successfully Updated')
            return redirect('accounts:profile')
        else:
            return render(request, 'accounts/change_profile_info.html', context={'form':form})

    form = form(instance=user)
    return render(request, 'accounts/change_profile_info.html', context = {'form': form})


@login_required
def change_password(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(user, request.POST)
        if form.is_valid():
            email = request.user.email
            form.save()
            update_session_auth_hash(request, user)
            messages.add_message(request, messages.SUCCESS, 'Your Password Has Been Successfully Updated')
            send_email_for_person(subject=email_messages['after_change_password']['subject'],
             message=email_messages['after_change_password']['message'], email=email)
            return redirect('accounts:profile')
        else:
            return render(request, 'registration/password_change_form.html', context = {'form': form})

    form = ChangePasswordForm(user)

    return render(request, 'registration/password_change_form.html', context = {'form': form})


@login_required
def contact_us(request):
    form = ContactUsForm()
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():

            email = request.user.email
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            send_contact_email_reply(subject, message, email)
            send_email_for_person(subject=email_messages['after_contact_us']['subject'], message=email_messages['after_contact_us']['message'], email=email)
            messages.add_message(request, messages.SUCCESS, 'Your message has been received and is being processed. We will get back to you as soon as possible.')

            return redirect('accounts:profile')

    return render(request, 'accounts/contact_us.html', {'form': form})

@login_required
def delete_account(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        return redirect('accounts:welcome_page')

    return render(request, 'delete_account.html')