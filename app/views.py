from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def contact_us(request):
    return render(request, 'contact_us.html')


def login(request):
    return render(request, 'login.html')