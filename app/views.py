from django.shortcuts import render, redirect
from .models import Student, Teacher, Questions
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
        image = request.FILES.get('image')
        user = request.POST['SelectUser']

        if user == 'student':
            standard = request.POST['standard']
            new = Student(name=name, standard=standard, username=username, password=password, mobile=mobile, image=image)
            new.save()
            messages.success(request, "Registration completed")
            return redirect(register)
        elif user == 'teacher':
            email = request.POST['email_id']
            new = Teacher(name=name, username=username, password=password, mobile=mobile, image=image, email=email)
            new.save()
            messages.success(request, "Registration completed")
            return redirect(register)
    else:
        return render(request, 'register.html')


def login_check(request):
    uname = request.POST['username']
    pword = request.POST['password']
    user = request.POST['user']
    if user == "teacher":
        if Teacher.objects.filter(username=uname,password=pword).exists():
            teacher_details = Teacher.objects.get(username=uname)
            request.session['name'] = teacher_details.name
            request.session['username'] = teacher_details.username
            request.session['password'] = teacher_details.password
            request.session['mobile'] = teacher_details.mobile
            request.session['email'] = teacher_details.email
            request.session['user'] = user
            request.session['id'] = teacher_details.id
            return render(request, 'teacher_dashboard.html')


def dashboard(request):
    if request.session['user'] == "teacher":
        return render(request, 'teacher_dashboard.html')
    else:
        pass


def my_account(request):
    if request.session['user'] == "teacher":
        user_id = request.session['id']
        user_details = Teacher.objects.get(id=user_id)
        return render(request, 'teacher_account.html', {'user':user_details})


def add_question(request):
    if request.method == "POST":
        qn = request.POST['question']
        op1 = request.POST['option1']
        op2 = request.POST['option2']
        op3 = request.POST['option3']
        op4 = request.POST['option4']
        correct = request.POST['correct_answer']
        new_qn = Questions(question=qn, option1=op1, option2=op2, option3=op3, option4=op4, correct_answer=correct)
        new_qn.save()
        return redirect(add_question)
    else:
        return render(request, 'add_question.html')


def logout(request):
    del request.session['name']
    del request.session['username']
    del request.session['password']
    del request.session['mobile']
    del request.session['email']
    del request.session['user']
    return redirect(home)