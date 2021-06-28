from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.urls import reverse

from .models import Student, Department, Teacher, Courses, Announcement, Forum , studyMaterial
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

my_group_student = Group.objects.get_or_create(name='Student')
my_group_teacher = Group.objects.get_or_create(name='Teacher')


def fun(request):
    g = request.user.groups.all()
    g_id = Group.objects.get(name=g[0]).id
    id = request.user.username
    if g_id == 1:
        student = Student.objects.filter(username=id)
        img = student[0].img

    else:
        teacher = Teacher.objects.filter(username=id)
        img = teacher[0].img
    return img, id


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
    messages.success(request, "Successfully logged out.")
    return HttpResponseRedirect(reverse('signIn'))


def mainPage(request):
    return render(request, 'ocp_app/mainPage.html')


@login_required
def home(request):
    id = request.user.username
    student = Student.objects.filter(username=id)
    img = student[0].img
    params = {'img': img, 'user': id}
    return render(request, 'ocp_app/home.html', params)


@login_required
def homeTeach(request):
    id = request.user.username
    teacher = Teacher.objects.filter(username=id)
    img = teacher[0].img
    params = {'img': img, 'user': id}
    return render(request, 'ocp_app/homeTeach.html', params)


@login_required
def dashboard(request):
    id = request.user.username
    student = Student.objects.filter(username=id)
    img = student[0].img
    params = {'img': img, 'user': id}
    return render(request, 'ocp_app/dashboard.html', params)


@login_required
def dashboardTeach(request):
    id = request.user.username
    teacher = Teacher.objects.filter(username=id)
    img = teacher[0].img
    params = {'img': img, 'user': id}
    return render(request, 'ocp_app/dashboardTeach.html', params)


def verifyOTP(request):
    if request.method == "POST":
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
            year = request.POST.get('year', '')
            email = request.POST.get('email', '')
            phone = request.POST.get('phone', '')
            password = request.POST.get('password', '')
            if int(enteredOTP) == int(otp):
                print('OTP verified')
                student = Student(img=img, username=username, firstname=firstname, lastname=lastname,
                                  dob=dob, dept=dept, email=email, phone=phone, password=password, year=year)
                student.save()
                myuser = User.objects.create_user(username, email, password)
                myuser.first_name = firstname
                myuser.last_name = lastname
                myuser.save()
                uname = User.objects.get(username=username)
                uid = uname.id
                user = User.objects.get(username=username)
                g = Group.objects.get(name='Student')
                g.user_set.add(uid)

                return render(request, 'ocp_app/verifyOTP.html', {'Valid_OTP': True})
            else:
                print('Invalid OTP')
                return render(request, 'ocp_app/verifyOTP.html', {'Invalid_OTP': True, 'OTP': otp, 'img': img, 'username': username, 'firstname': firstname, 'lastname': lastname, 'dob': dob, 'dept': dept, 'email': email, 'year': year, 'phone': phone, 'password': password})
        else:
            enteredOTP = request.POST.get('enteredOTP', '')
            otp = request.POST.get('otp', '')
            img = request.POST.get('img', '')
            username = request.POST.get('username', '')
            firstname = request.POST.get('firstname', '')
            lastname = request.POST.get('lastname', '')
            dob = request.POST.get('dob', '')
            dept1 = request.POST.getlist('dept', '')
            dept = ', '.join(dept1)
            designation = request.POST.get('designation', '')
            email = request.POST.get('email', '')
            phone = request.POST.get('phone', '')
            password = request.POST.get('password', '')
            if int(enteredOTP) == int(otp):
                print('OTP verified')
                teacher = Teacher(img=img, username=username, firstname=firstname, lastname=lastname,
                                  dob=dob, dept=dept, designation=designation, email=email, phone=phone, password=password)
                teacher.save()
                # Create user
                myuser = User.objects.create_user(username, email, password)
                myuser.first_name = firstname
                myuser.last_name = lastname
                myuser.save()
                uname = User.objects.get(username=username)
                uid = uname.id
                user = User.objects.get(username=username)
                g = Group.objects.get(name='Teacher')
                g.user_set.add(uid)

                return render(request, 'ocp_app/verifyOTP.html', {'Valid_OTP': True})
            else:
                print('Invalid OTP')
                return render(request, 'ocp_app/verifyOTP.html', {'Invalid_OTP': True, 'OTP': otp, 'img': img, 'username': username, 'firstname': firstname, 'lastname': lastname, 'dob': dob, 'dept': dept, 'designation': designation, 'email': email, 'phone': phone, 'password': password})
        return redirect('/signIn/')
    return render(request, 'ocp_app/verifyOTP.html')


def signUpStud(request):
    departments = Department.objects.all()
    if request.method == "POST" and request.FILES['file-input']:
        imgfile = request.FILES['file-input']
        fs = FileSystemStorage()
        imgfilename = fs.save(imgfile.name, imgfile)
        imgurl = fs.url(imgfilename)
        username = request.POST.get('username', '')
        firstname = request.POST.get('firstname', '')
        lastname = request.POST.get('lastname', '')
        dob = request.POST.get('dob', '')
        dept = request.POST.get('dept', '')
        email = request.POST.get('email', '')
        year = request.POST.get('year', '')
        phone = request.POST.get('phone', '')
        password = request.POST.get('password', '')
        cnfpassword = request.POST.get('confpassword', '')

        if not username.isalnum():
            messages.error(
                request, "Username must contain only letters or numbers.")
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
        if password != cnfpassword:
            messages.error(request, "Password does not match.")
            return redirect('/signUpStud/')
        if len(password) <= 8:
            messages.error(
                request, "Password should be greater than 8 characters.")
            return redirect('/signUpStud/')
        else:
            n1 = '\n'
            digits = "0123456789"
            OTP = ""
            for i in range(6):
                OTP += digits[math.floor(random.random() * 10)]
            subject = 'OTP Request'
            message = f'Hi {firstname} {lastname}, {n1}{n1}Welcome to the Online Classroom Portal.{n1}{n1}Your OTP is {OTP}. Do not share it with anyone by any means. This is confidential and to be used by you only.{n1}{n1}Warm regards,{n1}Online Classroom Portal(OCP)'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail(subject, message, email_from, recipient_list)
            params = {'img': imgurl, 'username': username, 'firstname': firstname, 'lastname': lastname, 'dob': dob,
                      'dept': dept, 'email': email, 'year': year, 'phone': phone, 'password': password, 'OTP': OTP}
            print('Mail sent! check your inbox.')
            return render(request, "ocp_app/verifyOTP.html", params)
    return render(request, 'ocp_app/signUpStud.html', {'departments': departments})


def signUpTeach(request):
    departments = Department.objects.all()
    if request.method == "POST" and request.FILES['file-input']:
        imgfile = request.FILES['file-input']
        fs = FileSystemStorage()
        imgfilename = fs.save(imgfile.name, imgfile)
        imgurl = fs.url(imgfilename)
        username = request.POST.get('username', '')
        firstname = request.POST.get('firstname', '')
        lastname = request.POST.get('lastname', '')
        dob = request.POST.get('dob', '')
        dept1 = request.POST.getlist('dept', '')
        dept = ', '.join(dept1)
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
        if password != cnfpassword:
            messages.error(request, "password does not match")
            return redirect('/signUpTeach/')
        else:
            n1 = '\n'
            digits = "0123456789"
            OTP = ""
            for i in range(6):
                OTP += digits[math.floor(random.random() * 10)]
            subject = 'OTP Request'
            message = f'Hi {firstname} {lastname}, {n1}{n1}Welcome to the Online Classroom Portal.{n1}{n1}Your OTP is {OTP}. Do not share it with anyone by any means. This is confidential and to be used by you only.{n1}{n1}Warm regards,{n1}Online Classroom Portal(OCP)'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail(subject, message, email_from, recipient_list)
            params = {'img': imgurl, 'username': username, 'firstname': firstname, 'lastname': lastname, 'dob': dob,
                      'dept': dept, 'designation': designation, 'email': email, 'phone': phone, 'password': password, 'OTP': OTP}
            print('Mail sent! check your inbox.')
            return render(request, "ocp_app/verifyOTP.html", params)
    return render(request, 'ocp_app/signUpTeach.html', {'departments': departments})


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
            g = request.user.groups.all()
            g_id = Group.objects.get(name=g[0]).id
            id = request.user.username
            if g_id == 1:
                student = Student.objects.filter(username=id)
                context["student"] = True
            else:
                teacher = Teacher.objects.filter(username=id)
                context["teacher"] = True
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
    g = request.user.groups.all()
    g_id = Group.objects.get(name=g[0]).id
    id = request.user.username
    if g_id == 1:
        student = Student.objects.filter(username=id)
        course = []
        if student != '\0':
            img = student[0].img
            cours = student[0].course
            arr = list(map(str, cours.strip().split()))
            for i in arr:
                courses = Courses.objects.get(course_id=i)
                course.append(courses)

    else:
        teacher = Teacher.objects.filter(username=id)
        img = teacher[0].img
        course = []
        if teacher != '\0':
            cours = teacher[0].course
            arr = list(map(str, cours.strip().split()))
            for i in arr:
                courses = Courses.objects.get(course_id=i)
                course.append(courses)

    if g_id == 1:
        template_values = 'ocp_app/dashboard.html'
    else:
        template_values = 'ocp_app/dashboardTeach.html'

    params = {'img': img, 'user': id, 'course': course,'my_template':template_values}
    return render(request, 'ocp_app/courseStud.html', params)


@login_required
def addCourse(request):
    g = request.user.groups.all()
    g_id = Group.objects.get(name=g[0]).id
    id = request.user.username
    if g_id == 1:
        student = Student.objects.filter(username=id)
        dept = ""
        course = []
        img = student[0].img
        year = student[0].year
        dept_name = student[0].dept
        cours = student[0].course
        arr = list(map(str, cours.strip().split()))
        for i in arr:
            courses = Courses.objects.get(course_id=i)
            course.append(courses)

        dept = Department.objects.filter(dept_name=dept_name).first()

        all_courses = Courses.objects.filter(year=year, dept=dept)

    else:
        teacher = Teacher.objects.filter(username=id)
        dept = []
        course = []
        all_courses = []
        img = teacher[0].img
        print(teacher)
        dep = teacher[0].dept
        print(dep)
        dept = list(map(str, dep.strip().split(',')))
        print(dept)
        cours = teacher[0].course
        arr = list(map(str, cours.strip().split()))
        for i in arr:
            courses = Courses.objects.get(course_id=i)
            course.append(courses)

        print(course)

        for element in dept:

            element = (element.strip())
            teach_courses = Courses.objects.filter(dept=element)
            print(teach_courses)
            for i in teach_courses:
                all_courses.append(i)

    new_course = []
    all_courses = list(all_courses)
    for i in (all_courses):
        if i not in course:
            new_course.append(i)
   # print(list(new_course) - course )
    print(new_course)
    if g_id == 1:
        template_values = 'ocp_app/dashboard.html'
    else:
        template_values = 'ocp_app/dashboardTeach.html'
    params = {'img': img, 'user': id, 'new_course': new_course,'my_template':template_values}
    return render(request, 'ocp_app/addCourse.html', params)


@login_required
def announcements(request):
    img, id = fun(request)
    announce = Announcement.objects.all()
    g = request.user.groups.all()
    g_id = Group.objects.get(name=g[0]).id
    if g_id == 1:
        template_values = 'ocp_app/dashboard.html'
    else:
        template_values = 'ocp_app/dashboardTeach.html'

    params = {'img': img, 'user': id, 'announce': announce,
              'my_template': template_values}
    return render(request, 'ocp_app/announcement.html', params)


@login_required
def addAnnouncements(request):
    img, id = fun(request)

    department = Teacher.objects.filter(username=id)
    dep = department[0].dept
    depart = []
    dept = list(map(str, dep.strip().split(',')))
    for i in dept:
        depart.append(i.strip())
    depart.sort()
    print(datetime.date.today(),
          datetime.datetime.now())
    print(timezone.now())
    params = {'img': img, 'user': id, 'dept': depart}
    return render(request, 'ocp_app/addAnnouncement.html', params)


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

        # date_of_announcement=datetime.date.today()
        # time_of_announcement=timezone.now
        dept = request.POST.get('dept', '')
        depart = Department.objects.get(dept_id=dept)
        announce = Announcement(announcement_name=name, detail=detail,
                                department=depart, file_type=file_type, announcement_file=imgurl)
        announce.save()
    return redirect(addAnnouncements)


@login_required
def updateProfile(request):
    img, id = fun(request)
    g = request.user.groups.all()
    g_id = Group.objects.get(name=g[0]).id
    id = request.user.username
    if g_id == 1:
        student = Student.objects.filter(username=id)
        fname = student[0].firstname
        lname = student[0].lastname
        dob = student[0].dob
        dept = student[0].dept
        email = student[0].email
        phone = student[0].phone
    else:
        student = Teacher.objects.filter(username=id)
        fname = student[0].firstname
        lname = student[0].lastname
        dob = student[0].dob
        dept = student[0].dept
        email = student[0].email
        phone = student[0].phone
    if g_id == 1:
        template_values = 'ocp_app/dashboard.html'
    else:
        template_values = 'ocp_app/dashboardTeach.html'
    params = {'img': img, 'user': id, 'firstname': fname,
              'lastname': lname, 'dob': dob, 'email': email, 'phone': phone,'my_template':template_values}
    if request.method == "POST" and 'fileToUpload' in request.FILES:
        imgfile = request.FILES['fileToUpload']
        fs = FileSystemStorage()
        imgfilename = fs.save(imgfile.name, imgfile)
        imgurl = fs.url(imgfilename)
        phone = request.POST.get('phone', '')
        dob = request.POST.get('dob', '')
        if g_id == 1:
            Student.objects.filter(username=id).update(
                img=imgurl, phone=phone, dob=dob)
            return HttpResponse("<script>setTimeout(function(){window.location.href='/updateProfile/'},0000);</script>")
        else:
            Teacher.objects.filter(username=id).update(
                img=imgurl, phone=phone, dob=dob)
            return HttpResponse("<script>setTimeout(function(){window.location.href='/updateProfile/'},0000);</script>")
    return render(request, 'ocp_app/updateProfile.html', params)


@login_required
def forum(request):
    img, id = fun(request)
    g = request.user.groups.all()
    g_id = Group.objects.get(name=g[0]).id
    id = request.user.username
    if g_id == 1:
        student = Student.objects.filter(username=id)
        name = student[0].firstname + ' ' + student[0].lastname
        email = student[0].email
    else:
        student = Teacher.objects.filter(username=id)
        name = student[0].firstname + ' ' + student[0].lastname
        email = student[0].email
    if g_id == 1:
        template_values = 'ocp_app/dashboard.html'
    else:
        template_values = 'ocp_app/dashboardTeach.html'
    params = {'img': img, 'user': id, 'name': name, 'email': email,'my_template':template_values}
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        r_email = request.POST.get('r_email','')
        subject = request.POST.get('subject', '')
        msg = request.POST.get('msg', '')
        # if g_id==1:
        print(name, email, subject, msg)
        forum = Forum(name=name, email=email, r_email=r_email, subject=subject, msg=msg)
        forum.save()
        return HttpResponse("<script>setTimeout(function(){window.location.href='/forum/'},0000);</script>")
    return render(request, 'ocp_app/forum.html', params)


@login_required
def add_course(request):
    if request.method == "GET":
        img, id = fun(request)
        cid = request.GET.get('sid')
        g = request.user.groups.all()
        g_id = Group.objects.get(name=g[0]).id
        if g_id == 1:
            print(cid)
            username = request.user.username
            student = Student.objects.filter(username=username)
            cours = student[0].course
            arr = list(map(str, cours.strip().split()))
            arr.append(cid)

            new_cours = ' '.join(arr)

            Student.objects.filter(username=id).update(course=new_cours)

            return JsonResponse({'status': 1})
        else:
            username = request.user.username
            teach = Teacher.objects.filter(username=username)
            cours = teach[0].course
            arr = list(map(str, cours.strip().split()))
            arr.append(cid)
            new_cours = ' '.join(arr)
            Teacher.objects.filter(username=id).update(course=new_cours)

            return JsonResponse({'status': 1})


@login_required
def del_course(request):
    if request.method == "GET":
        img, id = fun(request)

        params = {'img': img, 'user': id}
        g = request.user.groups.all()
        g_id = Group.objects.get(name=g[0]).id
        cid = request.GET.get('sid')
        print(cid)
        username = request.user.username
        if g_id == 1:
            student = Student.objects.filter(username=username)
            cours = student[0].course
            arr = list(map(str, cours.strip().split()))
            arr.remove(cid)
            new_cours = ' '.join(arr)
            Student.objects.filter(username=id).update(course=new_cours)

        else:

            teach = Teacher.objects.filter(username=username)
            cours = teach[0].course
            arr = list(map(str, cours.strip().split()))
            arr.remove(cid)
            new_cours = ' '.join(arr)
            Teacher.objects.filter(username=id).update(course=new_cours)

        return JsonResponse({'status': 1})


def view_material(request, cid):
    img, id = fun(request)
    course = Courses.objects.get(pk=cid)
    material = studyMaterial.objects.filter(course=course)
    g = request.user.groups.all()
    g_id = Group.objects.get(name=g[0]).id

    if g_id == 1:
        template_values = 'ocp_app/dashboard.html'
    else:
        template_values = 'ocp_app/dashboardTeach.html'

        params = {'img': img, 'user': id, 'material': material,
                  'my_template': template_values, 'course_id': cid}

        return render(request, 'ocp_app/view_study.html', params)


def addMaterial(request, cid):
    img, id = fun(request)
    params = {'img': img, 'user': id, 'course_id': cid}

    return render(request, 'ocp_app/add_material.html', params)


def add_Material(request, cid):
    img, id = fun(request)
    params = {'img': img, 'user': id}
    if request.method == "POST" and request.FILES['material_file']:
        file_type = request.POST.get('file_type', '')
        imgfile = request.FILES['material_file']
        if file_type == 'img':
            fs = FileSystemStorage()
            imgfilename = fs.save(imgfile.name, imgfile)
            imgurl = fs.url(imgfilename)
        else:
            imgurl = imgfile

        m_id = request.POST.get('m_id', '')

        detail = request.POST.get('detail', '')

        cours = Courses.objects.get(pk=cid)
        cours1 = Courses.objects.filter(pk=cid)

        dept = cours1[0].dept

        depart = Department.objects.filter(dept_id=dept)
        print(depart)
        material = studyMaterial(material_id=m_id, material_type=file_type, material_DESC=detail,
                                 material=imgurl, department=dept, course=cours, uploaded_by=id)
        material.save()

        params = {'img': img, 'user': id, 'course_id': cid}
        return render(request, 'ocp_app/add_material.html', params)


def viewStudent(request):
    img, id = fun(request)
    params = {'img': img, 'user': id}
    return render(request,'ocp_app/viewStudent.html',params)


def search_student(request):
    img, id = fun(request)

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

def view_query(request):
    img, id = fun(request)
    g = request.user.groups.all()
    g_id = Group.objects.get(name=g[0]).id

    query1 = Forum.objects.filter(email=request.user.email)
    query2 = Forum.objects.filter(r_email=request.user.email)

    if g_id == 1:
        template_values = 'ocp_app/dashboard.html'
    else:
        template_values = 'ocp_app/dashboardTeach.html'

    params = {'img': img, 'user': id,'query1':query1,'query2':query2,'my_template':template_values}

    return render(request,'viewQueries.html',params)
