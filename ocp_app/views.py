from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Student, Department, Teacher, Courses
from django.conf import settings 
from django.core.mail import send_mail 
import random
import math
from django.core.files.storage import FileSystemStorage


def user_login(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('user_success'))
        else:
            context["error"] = "Please enter valid username and password."
            return render(request, "ocp_app/login.html", context)
    else:
        return render(request, "ocp_app/login.html", context)

def success(request):
    context = {}
    context['user'] = request.user
    return render(request, "ocp_app/success.html", context)

def user_logout(request):
    logout(request)
    messages.success(request,"Successfully logged out.")
    return HttpResponseRedirect(reverse('signIn'))

def mainPage(request):
    return render(request, 'ocp_app/mainPage.html')

def verifyOTP(request):
    if request.method=="POST":
        designation = request.POST.get('designation', '')
        if designation == '':
            enteredOTP = request.POST.get('enteredOTP', '')
            otp = request.POST.get('otp', '')
            img = request.POST.get('img', '')
            username = request.POST.get('username', '')
            firstname = request.POST.get('firstname', '')
            lastname = request.POST.get('lastname', '')
            dob = request.POST.get('dob', '')
            dept = request.POST.get('dept', '')
            email = request.POST.get('email', '')
            phone = request.POST.get('phone', '')
            password = request.POST.get('password', '')
            if int(enteredOTP) == int(otp):
                print('OTP verified')
                student = Student(img=img,username=username,firstname=firstname,lastname=lastname,dob=dob,dept=dept,email=email,phone=phone,password=password)
                student.save()
                # Create user
                myuser = User.objects.create_user(username,email,password)
                myuser.first_name = firstname
                myuser.last_name = lastname
                myuser.save()
                return render(request, 'ocp_app/verifyOTP.html', {'Valid_OTP': True})
            else:
                print('Invalid OTP')
                return render(request, 'ocp_app/verifyOTP.html', {'Invalid_OTP': True,'OTP':otp,'img':img,'username':username,'firstname':firstname,'lastname':lastname,'dob':dob,'dept':dept,'email':email,'phone':phone,'password':password})
        else:
            enteredOTP = request.POST.get('enteredOTP', '')
            otp = request.POST.get('otp', '')
            img = request.POST.get('img', '')
            username = request.POST.get('username', '')
            firstname = request.POST.get('firstname', '')
            lastname = request.POST.get('lastname', '')
            dob = request.POST.get('dob', '')
            dept = request.POST.get('dept', '')
            c_id = request.POST.get('course_id', '')
            designation = request.POST.get('designation', '')
            email = request.POST.get('email', '')
            phone = request.POST.get('phone', '')
            password = request.POST.get('password', '')
            if int(enteredOTP) == int(otp):
                print('OTP verified')
                teacher = Teacher(img=img,username=username,firstname=firstname,lastname=lastname,dob=dob,dept=dept,designation=designation,course_id=c_id,email=email,phone=phone,password=password)
                teacher.save()
                # Create user
                myuser = User.objects.create_user(username,email,password)
                myuser.first_name = firstname
                myuser.last_name = lastname
                myuser.save()
                return render(request, 'ocp_app/verifyOTP.html', {'Valid_OTP': True})
            else:
                print('Invalid OTP')
                return render(request, 'ocp_app/verifyOTP.html', {'Invalid_OTP': True,'OTP':otp,'img':img,'username':username,'firstname':firstname,'lastname':lastname,'dob':dob,'dept':dept,'course_id':course_id,'designation':designation,'email':email,'phone':phone,'password':password})
        return redirect('/signIn/')
    return render(request, 'ocp_app/verifyOTP.html')

def signUpStud(request):
    departments = Department.objects.all()
    if request.method=="POST" and request.FILES['file-input']:
        imgfile = request.FILES['file-input']
        fs = FileSystemStorage()
        imgfilename = fs.save(imgfile.name,imgfile)
        imgurl = fs.url(imgfilename)
        username = request.POST.get('username', '')
        firstname = request.POST.get('firstname', '')
        lastname = request.POST.get('lastname', '')
        dob = request.POST.get('dob', '')
        dept = request.POST.get('dept', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        password = request.POST.get('password', '')
        cnfpassword = request.POST.get('confpassword', '')

        if not username.isalnum():
            messages.error(request, "Username must contain only letters or numbers.")
            return redirect('/signUpStud/')
        if firstname.isalpha() == False | lastname.isalpha() == False:
            messages.error(request, "Name must be alphabetical.")
            return redirect('/signUpStud/')
        if len(phone) != 10:
            messages.error(request, "Phone Number must be 10 digits.")
            return redirect('/signUpStud/')
        if phone.isdigit() == False:
            messages.error(request, "Phone Number must be numeric.")
            return redirect('/signUpStud/')
        if password!=cnfpassword:
            messages.error(request, "Password does not match.")
            return redirect('/signUpStud/')
        else:
            n1 = '\n'
            digits = "0123456789"
            OTP = "" 
            for i in range(6) : 
                OTP += digits[math.floor(random.random() * 10)]
            subject = 'OTP Request'
            message = f'Hi {firstname} {lastname}, {n1}{n1}Welcome to the Online Classroom Portal.{n1}{n1}Your OTP is {OTP}. Do not share it with anyone by any means. This is confidential and to be used by you only.{n1}{n1}Warm regards,{n1}Online Classroom Portal(OCP)'
            email_from = settings.EMAIL_HOST_USER 
            recipient_list = [email, ] 
            send_mail( subject, message, email_from, recipient_list ) 
            params = {'img':imgurl,'username':username,'firstname':firstname,'lastname':lastname,'dob':dob,'dept':dept,'email':email,'phone':phone,'password':password,'OTP':OTP}
            print('Mail sent! check your inbox.')
            return render(request, "ocp_app/verifyOTP.html", params)
    return render(request, 'ocp_app/signUpStud.html', {'departments':departments})

def signUpTeach(request):
    departments = Department.objects.all()
    courses = Courses.objects.all()
    if request.method=="POST" and request.FILES['file-input']:
        imgfile = request.FILES['file-input']
        fs = FileSystemStorage()
        imgfilename = fs.save(imgfile.name,imgfile)
        imgurl = fs.url(imgfilename)
        username = request.POST.get('username', '')
        firstname = request.POST.get('firstname', '')
        lastname = request.POST.get('lastname', '')
        dob = request.POST.get('dob', '')
        dept = request.POST.get('dept', '')
        designation = request.POST.get('designation', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        password = request.POST.get('password', '')
        cnfpassword = request.POST.get('confpassword', '')
        c_id = request.POST.get('courses','')

        if firstname.isalpha() == False | lastname.isalpha() == False:
            messages.error(request, "Name must be alphabetical")
            return redirect('/signUpTeach/')
        if len(phone) != 10:
            messages.error(request, "Phone Number must be 10 digits")
            return redirect('/signUpTeach/')
        if phone.isdigit() == False:
            messages.error(request, "Phone Number must be numeric")
            return redirect('/signUpTeach/')
        if password!=cnfpassword:
            messages.error(request, "password does not match")
            return redirect('/signUpTeach/')
        else:
            n1 = '\n'
            digits = "0123456789"
            OTP = "" 
            for i in range(6) : 
                OTP += digits[math.floor(random.random() * 10)]
            subject = 'OTP Request'
            message = f'Hi {firstname} {lastname}, {n1}{n1}Welcome to the Online Classroom Portal.{n1}{n1}Your OTP is {OTP}. Do not share it with anyone by any means. This is confidential and to be used by you only.{n1}{n1}Warm regards,{n1}Online Classroom Portal(OCP)'
            email_from = settings.EMAIL_HOST_USER 
            recipient_list = [email, ] 
            send_mail( subject, message, email_from, recipient_list )
            params = {'img':imgurl,'username':username,'firstname':firstname,'lastname':lastname,'dob':dob,'dept':dept,'designation':designation,'course_id':c_id,'email':email,'phone':phone,'password':password,'OTP':OTP}
            print('Mail sent! check your inbox.')
            return render(request, "ocp_app/verifyOTP.html", params)
    return render(request, 'ocp_app/signUpTeach.html', {'departments':departments,'courses':courses})


def signIn(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            context = {}
            context["user"] = request.user
            context["alert_flag"] = True
            return render(request, 'ocp_app/signIn.html', context)
        else:
            context["error"] = "Please enter valid username and password."
            context["alert_flag"] = False
            return render(request, "ocp_app/signIn.html", context)
    else:
        return render(request, "ocp_app/signIn.html", context)



