from django.shortcuts import render,redirect
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.urls import reverse
from .models import Student, Department, Teacher, Courses,Announcement
from django.contrib.auth.decorators import login_required
from django.conf import settings 
from django.core.mail import send_mail 
import random
import math
import datetime
from django.core.files.storage import FileSystemStorage


my_group_student = Group.objects.get_or_create(name='Student')
my_group_teacher = Group.objects.get_or_create(name='Teacher') 

def fun(request):
    g=request.user.groups.all()
    g_id=Group.objects.get(name=g[0]).id
    id=request.user.username
    if g_id==3:
            student=Student.objects.filter(username=id)    
            img=student[0].img

    else:
        teacher=Teacher.objects.filter(username=id)
        img=teacher[0].img
    return img,id

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

@login_required
def dashboard(request):
    id=request.user.username
    student=Student.objects.filter(username=id)
    img=student[0].img
    params={'img':img,'user':id}
    return render(request, 'ocp_app/dashboard.html',params)

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
            year = request.POST.get('year','')
            email = request.POST.get('email', '')
            phone = request.POST.get('phone', '')
            password = request.POST.get('password', '')
            if int(enteredOTP) == int(otp):
                print('OTP verified')
                student = Student(img=img,username=username,firstname=firstname,lastname=lastname,dob=dob,dept=dept,email=email,phone=phone,password=password,year=year)
                student.save()
                myuser = User.objects.create_user(username,email,password)
                myuser.first_name = firstname
                myuser.last_name = lastname
                myuser.save()
                uname=User.objects.get(username=username)
                uid=uname.id
                user=User.objects.get(username=username)
                g = Group.objects.get(name='Student')
                g.user_set.add(uid)

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
            dept1 = request.POST.getlist('dept', '')
            dept=', '.join(dept1)
            designation = request.POST.get('designation', '')
            email = request.POST.get('email', '')
            phone = request.POST.get('phone', '')
            password = request.POST.get('password', '')
            if int(enteredOTP) == int(otp):
                print('OTP verified')
                teacher = Teacher(img=img,username=username,firstname=firstname,lastname=lastname,dob=dob,dept=dept,designation=designation,email=email,phone=phone,password=password)
                teacher.save()
                # Create user
                myuser = User.objects.create_user(username,email,password)
                myuser.first_name = firstname
                myuser.last_name = lastname
                myuser.save()
                uname=User.objects.get(username=username)
                uid=uname.id
                user=User.objects.get(username=username)
                g = Group.objects.get(name='Teacher')
                g.user_set.add(uid)
                
                return render(request, 'ocp_app/verifyOTP.html', {'Valid_OTP': True})
            else:
                print('Invalid OTP')
                return render(request, 'ocp_app/verifyOTP.html', {'Invalid_OTP': True,'OTP':otp,'img':img,'username':username,'firstname':firstname,'lastname':lastname,'dob':dob,'dept':dept,'designation':designation,'email':email,'phone':phone,'password':password})
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
    if request.method=="POST" and request.FILES['file-input']:
        imgfile = request.FILES['file-input']
        fs = FileSystemStorage()
        imgfilename = fs.save(imgfile.name,imgfile)
        imgurl = fs.url(imgfilename)
        username = request.POST.get('username', '')
        firstname = request.POST.get('firstname', '')
        lastname = request.POST.get('lastname', '')
        dob = request.POST.get('dob', '')
        dept1 = request.POST.getlist('dept', '')
        dept=', '.join(dept1)
        designation = request.POST.get('designation', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        password = request.POST.get('password', '')
        cnfpassword = request.POST.get('confpassword', '')

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
            params = {'img':imgurl,'username':username,'firstname':firstname,'lastname':lastname,'dob':dob,'dept':dept,'designation':designation,'email':email,'phone':phone,'password':password,'OTP':OTP}
            print('Mail sent! check your inbox.')
            return render(request, "ocp_app/verifyOTP.html", params)
    return render(request, 'ocp_app/signUpTeach.html', {'departments':departments})


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

def signOut(request):
    logout(request)
    return redirect(signIn)

@login_required
def courseStud(request):
    g=request.user.groups.all()
    g_id=Group.objects.get(name=g[0]).id
    id=request.user.username
    if g_id==3:
        student=Student.objects.filter(username=id)
        course=[]
        dept=""
        if student!='\0':
            img=student[0].img
            for i in student:
                courses = i.course
                course.append(courses)
    
    
    else:
        teacher=Teacher.objects.filter(username=id)
        img=teacher[0].img

    params={'img':img,'user':id,'course':course}
    return render (request,'ocp_app/courseStud.html',params)

@login_required
def addCourse(request):
    g=request.user.groups.all()
    g_id=Group.objects.get(name=g[0]).id
    id=request.user.username
    if g_id==3:
        student=Student.objects.filter(username=id)    
        dept=""
        img=student[0].img
        year = student[0].year
        dept_name=student[0].dept
    else: 
        teacher=Teacher.objects.filter(username=id)
        dept=""
        img=teacher[0].img
        year = teacher[0].year
        dept_name=student[0].dept

    dept=Department.objects.filter(dept_name=dept_name).first()
    new_course=Courses.objects.filter(year=year,dept=dept)
    print(new_course)

    params={'img':img,'user':id,'new_course':new_course}
    return render(request,'ocp_app/addCourse.html',params)


@login_required
def announcements(request):
    img,id=fun(request)
    announce=Announcement.objects.all()
    
    params={'img':img,'user':id,'announce':announce}
    return render(request,'ocp_app/announcement.html',params)


def newannouncements(request):
    department=Department.objects.all()
    params={'department':department}
    return render(request,'ocp_app/add_announcement.html',params)

def addAnnouncements(request):
    if request.method=="POST" and request.FILES['announce_file']:
        name = request.POST.get('name', '')
        detail = request.POST.get('detail', '')
        imgfile = request.FILES['announce_file']
        fs = FileSystemStorage()
        imgfilename = fs.save(imgfile.name,imgfile)
        imgurl = fs.url(imgfilename)
        dept = request.POST.get('dept', '')
        print(dept)
        department=Department.objects.filter(dept_name='Computer Science and Engineering')
        dept_id=department[0].dept_id
        print(department)
        date=datetime.date.today()
        time=datetime.datetime.now()
        
        announce=Announcement(announcement_name=name,detail=detail,announcement_file=imgurl,date_of_announcement=date,time_of_announcement=time)
        announce.save()
        return redirect(newannouncements)
    


