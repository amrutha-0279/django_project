from django.shortcuts import render,redirect
from student.models import *
import uuid
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.hashers import make_password


# Create your views here

def register(request):
    if request.method == "POST":
        try:
            email = request.POST.get('email')

            if Student.objects.filter(email=email).exists():
                return render(request, 'accounts/register.html', {
                    'msg': 'Email already exists'
                })

            token = str(uuid.uuid4())

            student = Student.objects.create(
                first_name=request.POST.get('fname'),
                last_name=request.POST.get('lname'),
                gender=request.POST.get('gender'),
                dob=request.POST.get('dob'),
                email=email,
                phone=request.POST.get('phone'),
                state=request.POST.get('state'),
                city=request.POST.get('city'),
                hobbies=",".join(request.POST.getlist('hobbies')),
                password=request.POST.get('password'),
                token=token
            )

            if 'images' in request.FILES:
                student.photo = request.FILES['images']
                student.save()
            #link = request.build_absolute_uri(f"/accounts/verify/{token}/")
            from django.urls import reverse

            link = request.build_absolute_uri(
            reverse('verify', args=[token])
            )
            send_mail(
                "Verify Email",
                f"Click to verify your account:\n{link}",
                "amruthaalphonsa02@gmail.com",
                [student.email]
)

            return render(request, 'accounts/register.html', {
                'msg': 'Registered successfully! Check your email.'
            })

        except Exception as e:
            print("ERROR:", e)
            return render(request, 'accounts/register.html', {
                'msg': 'Registration failed. Please try again.'
            })

    return render(request, 'accounts/register.html')




from django.contrib.auth.hashers import check_password




from django.contrib.auth.hashers import check_password, make_password

from django.contrib.auth.hashers import check_password, make_password

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Student.objects.get(email=email)

            # ❌ not verified
            if not user.is_verified:
                return render(request, 'accounts/login.html', {
                    'error': 'Please verify your email first'
                })

            # ✅ FIRST TIME → send temp password ONLY ONCE
            if user.first_login and not user.temp_password_sent:
                temp_pass = str(uuid.uuid4())[:8]

                user.password = make_password(temp_pass)
                user.temp_password_sent = True   # ✅ important
                user.save()

                send_mail(
                    "Temporary Password",
                    f"Your temp password is: {temp_pass}",
                    'your_email@gmail.com',
                    [user.email]
                )

                return render(request, 'accounts/login.html', {
                    'error': 'Temp password sent to your email'
                })

            # ✅ CHECK PASSWORD
            if not check_password(password, user.password):
                return render(request, 'accounts/login.html', {
                    'error': 'Invalid email or password'
                })

            # ✅ SESSION
            request.session['user'] = user.id

            # ✅ FORCE PASSWORD CHANGE (FIRST LOGIN)
            if user.first_login:
                return redirect('set_new_password')

            return redirect('dashboard')

        except Student.DoesNotExist:
            return render(request, 'accounts/login.html', {
                'error': 'Invalid email or password'
            })

    return render(request, 'accounts/login.html')

def ForgotPassword(request):
    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user = Student.objects.get(email=email)

            # generate temp password
            temp_pass = str(uuid.uuid4())[:8]   # shorter password

            user.password = temp_pass
            user.save()
            
            # send email
            send_mail(
                "Temporary Password",
                f"Your temporary password is: {temp_pass}",
                "amruthaalphonsa02@gmail.com",
                [email]
            )

            return render(request, 'accounts/login.html', {
                'msg': 'Temporary password sent to your email'
            })

        except Student.DoesNotExist:
            return render(request, 'accounts/forgot.html', {
                'error': 'Email not found'
            })

        except Exception as e:
            print("ERROR:", e)
            return render(request, 'accounts/forgot.html', {
                'error': 'Something went wrong'
            })

    return render(request, 'accounts/forgot.html')
from django.shortcuts import render
from student.models import Student

def verify(request, token):
    try:
        user = Student.objects.get(token=token)
        user.is_verified = True
        user.save()

        return render(request, 'accounts/login.html', {
            'msg': 'Email verified successfully! Please login.'
        })

    except:
        return render(request, 'accounts/login.html', {
            'msg': 'Invalid or expired link'
        })
    from django.shortcuts import redirect

def logout_view(request):
    request.session.flush()  # clear session data

    response = redirect('login')
    response.delete_cookie('user')  # remove "remember me" cookie

    return response
def set_new_password(request):
    if request.method == "POST":
        new_password = request.POST.get('password')

        user_id = request.session.get('user')
        user = Student.objects.get(id=user_id)

        from django.contrib.auth.hashers import make_password
        user.password = make_password(new_password)
        user.first_login = False   # ✅ important
        user.save()

        return redirect('dashboard')

    return render(request, 'accounts/set_new_password.html')    