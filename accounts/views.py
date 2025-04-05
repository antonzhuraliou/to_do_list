from .forms import LoginForm, RegisterForm
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings


def get_welcome_page(request):
    return render(request, 'accounts/welcome_page.html')


def custom_login_view(request):
    form = LoginForm
    if request.method == "POST":
        form = LoginForm(request.POST)
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            user_obj = None

        if user_obj:
            user = authenticate(request, username=user_obj.username, password=password)
            if user is not None:
                login(request, user)
                return redirect("tasks:main_page")
            else:
                error = "Неверный пароль"
        else:
            error = "Пользователь с таким email не найден"

        return render(request, "registration/login.html", {"error": error, 'form': form})
    return render(request, "registration/login.html", {'form': form})


def get_profile(request):
    return render(request, 'accounts/profile.html')

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

