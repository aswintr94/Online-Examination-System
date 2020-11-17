from django.contrib import admin
from .models import Student, Teacher, Questions, Results

# Register your models here.
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Questions)
admin.site.register(Results)