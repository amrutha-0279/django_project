
from django.shortcuts import render, redirect
from student.models import Student, Course,Enrollment
from django.contrib.auth.hashers import check_password, make_password
def dashboard(request):
# Create your views here.
    if not request.session.get('user'):
        return redirect('/login/')
    user_id = request.session.get('user')
    courses=Course.objects.all()
    student = Student.objects.get(id=user_id)
    return render(request,'dashboard.html',{'courses':courses,'student':student})
def logout(request):
    request.session.flush()
    response=redirect('/login/')
    response.delete_cookie('user_id')
    return response
def course_list(request):
    student_id = request.session.get('user')
    if not student_id:
        return redirect('login')

    courses = Course.objects.all()

    return render(request, 'courses.html', {
        'courses': courses
    })


def my_courses(request):
    if 'user' not in request.session:
        return redirect('login')

    student = Student.objects.get(id=request.session['user'])

    enrollments = Enrollment.objects.filter(student=student)

    return render(request, 'my_courses.html', {
        'enrollments': enrollments
    })

def update_profile(request):
    student_id = request.session.get('user')
    student = Student.objects.get(id=student_id)

    if request.method == "POST":
        student.first_name = request.POST['first_name']
        student.last_name = request.POST['last_name']
        student.phone = request.POST['phone']
        student.city = request.POST['city']
        student.state = request.POST['state']
        student.save()

        return redirect('profile')

    return render(request, 'profile.html', {'student': student})
def change_password(request):
    student_id = request.session.get('user')
    student = Student.objects.get(id=student_id)

    if request.method == "POST":
        old = request.POST['old_password']
        new = request.POST['new_password']

        if check_password(old, student.password):
            student.password = make_password(new)
            student.save()

            # AUTO LOGOUT
            request.session.flush()

            response = redirect('login')
            response.delete_cookie('user')

            return response

        else:
            return render(request, 'change_password.html', {
                'error': 'Old password incorrect'
            })

    return render(request, 'change_password.html')



# views.py

def courses(request):
    query = request.GET.get('q')

    if query:
        courses = Course.objects.filter(name__icontains=query)
    else:
        courses = Course.objects.all()

    msg = request.GET.get('msg')

    return render(request, 'student/courses.html', {
        'courses': courses,
        'msg': msg
    })
def signup_course(request, course_id):
    user_id = request.session.get('user')

    if not user_id:
        return redirect('login')

    student = Student.objects.get(id=user_id)
    course = Course.objects.get(id=course_id)

    # check already enrolled
    if Enrollment.objects.filter(student=student, course=course).exists():
        return redirect('/student/courses/?msg=Already Enrolled')

    Enrollment.objects.create(student=student, course=course)

    return redirect('/student/courses/?msg=Successfully Enrolled')

    return render(request, 'profile.html', {'student': student})
def profile(request):
    if 'user' not in request.session:
        return redirect('login')

    student = Student.objects.get(id=request.session['user'])
    success = False

    if request.method == "POST":
        student.name = request.POST.get('name')
        student.email = request.POST.get('email')
        student.phone = request.POST.get('phone')
        student.address = request.POST.get('address')

        if request.FILES.get('photo'):
            student.photo = request.FILES.get('photo')

        student.save()
        success = True

    return render(request, 'profile.html', {
        'student': student,
        'success': success
    })