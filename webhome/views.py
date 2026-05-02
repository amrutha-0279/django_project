from django.shortcuts import render
from .models import *
from django.core.mail import send_mail
from student.models import Course
# Create your views here.
    # if request.method=="POST":
    #     try:
    #         Contact.objects.create(
    #             name=request.POST['name'],
    #             email=request.POST['email'],
    #             subject=request.POST['subject'],
    #             message=request.POST['message']
    #         )
            # send_mail(
            #     request.POST['subject'],
            #     request.POST['message'],
            #     request.POST['email',['amruthaalphonsa02@gmail.com']]
            # )
#             
from django.core.mail import EmailMessage

def contact(request):
    if request.method == "POST":

        name = request.POST['name']
        student_email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        email = EmailMessage(
            subject=f"New Message from {name}",
            body=f"""
Student Contact Details:

Name: {name}
Email: {student_email}

Message:
{message}
""",
            from_email='amruthaalphonsa02@gmail.com',   # institute email
            to=['amruthaalphonsa02@gmail.com'],         # institute email
            reply_to=[student_email]   
        )

        email.send()

        return render(request, 'webhome/contact.html', {'msg': 'Message sent successfully'})

    return render(request, 'webhome/contact.html')
def home(request):
    course=Course.objects.all()
    return render(request,'webhome/home.html',{'course':course})
def about(request):
    return render(request,'webhome/about.html')