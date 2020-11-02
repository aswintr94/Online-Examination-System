from django.shortcuts import render, redirect
from .models import Student, Teacher
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def contact_us(request):
    return render(request, 'contact_us.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        name = request.POST['name']
        username = request.POST['username']
        password = request.POST['password']
        mobile = request.POST['mobile']
        image = request.POST['image']
        user = request.POST['SelectUser']

        if user == 'student':
            standard = request.POST['standard']
            new = Student(name=name, standard=standard, username=username, password=password, mobile=mobile, image=image)
            new.save()
            return redirect(register)
        elif user == 'teacher':
            email = request.POST['email_id']
            new = Teacher(name=name, username=username, password=password, mobile=mobile, image=image, email=email)
            new.save()
            return redirect(register)
    else:
        return render(request, 'register.html')