from django.db import models

# Create your models here.


class Student(models.Model):
    name = models.CharField(max_length=30)
    standard = models.IntegerField(null=True)
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=10)
    mobile = models.CharField(max_length=15)
    image = models.FileField(upload_to='students', null=True)


class Teacher(models.Model):
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=10)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(null=True)
    image = models.FileField(upload_to='teachers')


class Questions(models.Model):
    question = models.TextField()
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    correct_answer = models.CharField(max_length=100)