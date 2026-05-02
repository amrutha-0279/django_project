from django.contrib import admin
from .models import *
admin.site.register(Student)
# Register your models here.
admin.site.register(Course)
admin.site.register(Enrollment)