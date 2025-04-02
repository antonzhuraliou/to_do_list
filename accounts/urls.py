from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('', views.get_welcome_page, name='welcome_page'),

]