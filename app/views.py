from django.shortcuts import render, redirect
from .models import Student, Teacher, Questions, Results
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError


# Create your views here.
def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def contact_us(request):
    return render(request, 'contact_us.html')


def login(request):
    if request.method == "POST":
        uname = request.POST['username']
        pword = request.POST['password']
        user = request.POST['user']
        if user == "teacher":
            if Teacher.objects.filter(username=uname, password=pword).exists():
                teacher_details = Teacher.objects.get(username=uname)
                request.session['name'] = teacher_details.name
                request.session['username'] = teacher_details.username
                request.session['password'] = teacher_details.password
                request.session['mobile'] = teacher_details.mobile
                request.session['email'] = teacher_details.email
                request.session['user'] = user
                request.session['id'] = teacher_details.id
                return render(request, 'teacher_dashboard.html')
            else:
                messages.error(request, "Check your username and password")
                return redirect(login)
        else:
            if Student.objects.filter(username=uname, password=pword).exists():
                student_details = Student.objects.get(username=uname)
                request.session['name'] = student_details.name
                request.session['username'] = student_details.username
                request.session['password'] = student_details.password
                request.session['mobile'] = student_details.mobile
                request.session['email'] = student_details.email
                request.session['user'] = user
                request.session['id'] = student_details.id
                return render(request, 'student_dashboard.html')
            else:
                messages.error(request, "Check your username and password")
                return redirect(login)
    else:
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


def dashboard(request):
    if request.session['user'] == "teacher":
        return render(request, 'teacher_dashboard.html')
    else:
        return render(request, 'student_dashboard.html')


def my_account(request):
    if request.session['user'] == "teacher":
        user_id = request.session['id']
        user_details = Teacher.objects.get(id=user_id)
        return render(request, 'my_account.html', {'user': user_details})
    else:
        user_id = request.session['id']
        user_details = Student.objects.get(id=user_id)
        return render(request, 'my_account.html', {'user': user_details})


def update_user_info(request):
    if request.session['user'] == "teacher":
        if request.method == "POST":
            name = request.POST.get('name')
            username = request.POST.get('username')
            mobile = request.POST.get('mobile')
            email = request.POST.get('email_id')
            try:
                image = request.FILES['image']
                fs = FileSystemStorage()
                loc = "teachers/%s"%image.name
                image = fs.save(loc, image)
            except MultiValueDictKeyError:
                user = Teacher.objects.get(id = request.session.get('id'))
                image = user.image

            Teacher.objects.filter(id=request.session.get('id')).update(name=name, username=username, mobile=mobile, email=email, image=image)
            return redirect(my_account)
        else:
            user_info = Teacher.objects.get(id=request.session.get('id'))
            return render(request, 'update.html', {'user_info': user_info})
    else:
        if request.method == "POST":
            name = request.POST.get('name')
            username = request.POST.get('username')
            mobile = request.POST.get('mobile')
            email = request.POST.get('email_id')
            try:
                image = request.FILES['image']
                fs = FileSystemStorage()
                loc = "students/%s"%image.name
                image = fs.save(loc, image)
            except MultiValueDictKeyError:
                user = Student.objects.get(id=request.session.get('id'))
                image = user.image
            Student.objects.filter(id=request.session.get('id')).update(name=name, username=username, email=email, mobile=mobile, image=image)
            return redirect(my_account)
        else:
            user_info = Student.objects.get(id=request.session.get('id'))
            return render(request, 'update.html', {'user_info': user_info})


def change_password(request):
    if request.method == "POST":
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        email_id = request.POST.get('email_id')
        if request.session['user'] == "teacher":
            if Teacher.objects.filter(password=current_password, email=email_id).exists():
                Teacher.objects.filter(password=current_password, email=email_id).update(password=new_password)
                messages.success(request, "Password changed successfully")
                return redirect(my_account)
            else:
                messages.error(request, "You entered a wrong password")
                return redirect(my_account)
        else:
            if Student.objects.filter(password=current_password, email=email_id).exists():
                Student.objects.filter(password=current_password, email=email_id).update(password=new_password)
                messages.success(request, "Password changed successfully")
                return redirect(my_account)
            else:
                messages.error(request, "You entered a wrong password")
                return redirect(my_account)
    else:
        return render(request, 'change_password.html')


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


def view_questions(request):
    questions = Questions.objects.all()
    return render(request, 'questions.html', {'questions': questions})


def delete_all_questions(request):
    questions = Questions.objects.all()
    questions.delete()
    return redirect(add_question)


def delete_question(request, q_id):
    question = Questions.objects.get(id=q_id)
    question.delete()
    return redirect(view_questions)


def view_students(request):
    students = Student.objects.all()
    return render(request, 'student_report.html', {'students': students})


def attend_exam(request):
    if request.method == "POST":
        temp = 0
        your_answers = dict()
        questions = Questions.objects.all()
        for i in questions:
            option = str(i.id) + 'option'
            selected_answer = request.POST.get(option)
            correct_answer = request.POST.get(str(i.id) + 'correct')
            if selected_answer == correct_answer:
                temp += 1
        student = Student.objects.get(id=request.session['id'])
        marks = str(temp) + " out of " + str(len(questions))
        if Results.objects.filter(student_id__name=request.session['name']).exists():
            messages.warning(request, "You have already attended the exam")
            return redirect(my_results)
        else:
            result = Results(student=student, marks=marks)
            result.save()
            questions = Questions.objects.all()
            return render(request, 'exam_analysis.html',
                          {'questions': questions, 'marks': temp, 'number': len(questions)})
    else:
        questions = Questions.objects.all()
        return render(request, 'exam.html', {'questions': questions})


def my_results(request):
    result = Results.objects.get(student_id__name=request.session['name'])
    return render(request, 'my_result.html', {'result': result})


def all_results(request):
    result = Results.objects.all()
    return render(request, 'all_results.html', {'results': result})


def delete_results(request):
    results = Results.objects.all()
    results.delete()
    return redirect(add_question)


def logout(request):
    del request.session['name']
    del request.session['username']
    del request.session['password']
    del request.session['mobile']
    del request.session['email']
    del request.session['user']
    return redirect(home)