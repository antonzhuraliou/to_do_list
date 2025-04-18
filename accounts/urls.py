from django.urls import path
from accounts import views


app_name = 'accounts'

urlpatterns = [
    path('', views.get_welcome_page, name='welcome_page'),
    path('login/', views.custom_login_view, name='login'),
    path('profile/', views.get_profile, name = 'profile'),
    path('register/', views.get_register, name = 'register'),
    path('change_username/<str:change>/', views.change_username, name='change_username'),
    path('change-password/', views.change_password, name = 'change_password'),
    path('contact_us/', views.contact_us, name='contact'),
    path('delete_account/', views.delete_account, name='delete_account')
]