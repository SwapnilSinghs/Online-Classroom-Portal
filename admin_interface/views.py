from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.urls import reverse

from ocp_app.models import Student, Department, Teacher, Courses, Announcement, Forum , studyMaterial
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
import random
import math
from django.utils import timezone
import datetime
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.http import FileResponse, Http404

# Create your views here.
def home(request):
    return render(request,'login.html')


@login_required
def admin_dashboard(request):
    id=request.user.username
    total_dep=Department.objects.all().count()
    total_stud=Student.objects.all().count()
    total_fac=Teacher.objects.all().count()
    total_course=Courses.objects.all().count()



    params={'user':id,"total_dep":total_dep,"total_stud":total_stud,"total_fac":total_fac,"total_course":total_course}

    return render(request, 'admin_dashboard.html',params)


def signinhandle(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['pass']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
        
    return redirect(admin_dashboard)



def signup(request):
    return render(request,'signup.html')

def signOut(request):
    logout(request)
    return redirect(admin/home)


def signuphandle(request):
    if request.method =="POST":
        username = "admin123"
        firstname = request.POST.get('firstname', '')
        lastname = request.POST.get('lastname', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        confirm_pass = request.POST.get('confirm_pass', '')

        if not username.isalnum():
            messages.error(request, "Username must contain only letters or numbers.")
            return redirect('/admin/signup/')
        if firstname.isalpha() == False | lastname.isalpha() == False:
            messages.error(request, "Name must be alphabetical.")
            return redirect('/admin/signup/')
       
        if password!=confirm_pass:
            messages.error(request, "Password does not match.")
            return redirect('/admin/signup/')
        if len(password)<=8:
            messages.error(request, "Password should be greater than 8 characters.")
            return redirect('/admin/signup/')

        myuser = User.objects.create_user(username,email,password)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.save()

        return render(request,'home.html')



@login_required
def viewAnnouncements(request):
    id = request.user.username
    announce = Announcement.objects.all()
    params = {'user': id, 'announce': announce}
    return render(request, 'viewAnnouncement.html', params)

@login_required
def addAnnouncements(request):
    id = request.user.username
    department = Department.objects.all()
    depart=[]
    for i in department:
        depart.append(i.dept_id)
    
    params = { 'user': id, 'dept': depart}
    return render(request, 'addAnnouncement.html', params)

def add_announcement(request):
    if request.method == "POST" and request.FILES['announce_file']:
        file_type = request.POST.get('file_type', '')
        imgfile = request.FILES['announce_file']
        if file_type == 'img':
            fs = FileSystemStorage()
            imgfilename = fs.save(imgfile.name, imgfile)
            imgurl = fs.url(imgfilename)
        else:
            imgurl = imgfile
        name = request.POST.get('name', '')
        detail = request.POST.get('detail', '')
        file_type = request.POST.get('file_type', '')
        dept = request.POST.get('dept', '')
        depart = Department.objects.get(dept_id=dept)
        announce = Announcement(announcement_name=name, detail=detail,
                                department=depart, file_type=file_type, announcement_file=imgurl)
        announce.save()
    return redirect('../addAnnouncement')


def del_announce(request):
    if request.method == "GET":
        aid=request.GET.get('sid','')
        print(aid)
        announce = Announcement.objects.get(announcement_id = aid)
        announce.delete()
        return JsonResponse({'status': 1})

    else:
        return JsonResponse({'status': 0})


def createDepartment(request):
    return render(request,'createDepartment.html')

def create_Department(request):
    if request.method == "POST":
        dept_id=request.POST.get('dept_id','')
        dept_name = request.POST.get('dept_name','')

        if dept_id =="" or dept_name=="":
            return redirect('../createDepartment')

        depart=Department(dept_id=dept_id,dept_name=dept_name)

        depart.save()

    return redirect('../createDepartment')


def viewDepartment(request):
    id = request.user.username
    depart=Department.objects.all()
    print(depart)
    params={'user':id,'department':depart}
    return render(request,'viewDepartment.html',params)


def del_department(request):
    if request.method == "GET":
        did=request.GET.get('sid','')
        print(did)
        depart = Department.objects.get(dept_id = did)
        depart.delete()
        return JsonResponse({'status': 1})

    else:
        return JsonResponse({'status': 0})


def viewStudent(request):
    id = request.user.username
    params = {'user': id}
    return render(request,'viewStudent.html',params)


def search_student(request):
    id = request.user.username

    if request.method == 'GET':
        sname=request.GET.get('sid','')
        print(sname)
        student=Student.objects.filter(username=sname).values()
        student_data=list(student)
        
        if student :
           
            return JsonResponse({'status': 1 , 'student':student_data})

        else:
            return JsonResponse({'status': 0})

    else:
        return JsonResponse({'status': 0})

def viewFaculty(request):
    id = request.user.username
    params = {'user': id}
    return render(request,'viewFaculty.html',params)


def search_faculty(request):
    id = request.user.username

    if request.method == 'GET':
        sname=request.GET.get('sid','')
        print(sname)
        teacher=Teacher.objects.filter(username=sname).values()
        teacher_data=list(teacher)
        
        if teacher :
           
            return JsonResponse({'status': 1 , 'teacher':teacher_data})

        else:
            return JsonResponse({'status': 0})

    else:
        return JsonResponse({'status': 0})



def del_student(request):
    if request.method == "GET":
        sid=request.GET.get('sid','')
        print(sid)
        student = Student.objects.get(username = sid)
        student.delete()
        return JsonResponse({'status': 1})

    else:
        return JsonResponse({'status': 0})

def del_teacher(request):
    if request.method == "GET":
        fid=request.GET.get('sid','')
        print(fid)
        teacher = Teacher.objects.get(username = fid)
        teacher.delete()
        return JsonResponse({'status': 1})

    else:
        return JsonResponse({'status': 0})