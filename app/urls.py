from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('login_check/', views.login_check, name='login_check'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('my_account/', views.my_account, name='my_account'),
    path('add_question/', views.add_question, name='add_question'),
    path('view_questions/', views.view_questions, name='view_questions'),
    path('view_students/', views.view_students, name='view_students'),
    path('attend_exam/', views.attend_exam, name='attend_exam'),
    path('check_answers/', views.check_answers, name='check_answers'),
    path('my_results/', views.my_results, name='my_results'),
    path('logout/', views.logout, name='logout'),
]