from django.shortcuts import render

def get_welcome_page(request):
    return render(request, 'accounts/welcome_page.html')