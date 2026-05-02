from django.db import models
class Student(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    dob=models.DateField()
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=15)
    state=models.CharField(max_length=25)
    city=models.CharField(max_length=15,default='Trivandrum')
    hobbies=models.CharField(max_length=200)
    photo=models.ImageField(upload_to='images/')
    password=models.CharField(max_length=200)
    is_verified=models.BooleanField(default=False)
    token=models.CharField(max_length=200)
    courses = models.ManyToManyField('Course', blank=True)
    first_login = models.BooleanField(default=True)
    temp_password_sent = models.BooleanField(default=False)
    address = models.TextField(blank=True)
class Course(models.Model):
    name=models.CharField(max_length=100)
    duration=models.CharField(max_length=50)
    fee=models.IntegerField()
    def __str__(self):
        return self.name
class Enrollment(models.Model):
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)   
    
    