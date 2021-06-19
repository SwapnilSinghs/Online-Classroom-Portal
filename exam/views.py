from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from ocp_app.models import Student, Department, Teacher, Courses, Announcement, Forum
from exam.models import Exam, Assignment
from django.http import HttpResponse
# Create your views here.


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


def examDashboard(request):
    return render(request, 'examDashboard.html')


def addAssignment(request):
    img, id = fun(request)
    g = request.user.groups.all()
    g_id = Group.objects.get(name=g[0]).id
    id = request.user.username
    if g_id == 1:
        return render(request, 'examDashboard.html')
    else:
        teacher = Teacher.objects.filter(username=id)
        uploadedBy = teacher[0].firstname + ' ' + teacher[0].lastname
        courses = Courses.objects.all()
        departments = Department.objects.all()
    params = {'uploadedBy': uploadedBy,
              'courses': courses, 'departments': departments}
    if request.method == "POST" and request.FILES['assign_file']:
        assignfile = request.FILES['assign_file']
        fileurl = assignfile
        assign_name = request.POST.get('assign_name', '')
        doa = request.POST.get('doa', '')
        ast = request.POST.get('ast', '')
        aet = request.POST.get('aet', '')
        cname = request.POST.get('course', '')
        course = Courses.objects.get(course_name=cname)
        dept = request.POST.get('dept', '')
        uploadedBy = request.POST.get('uploadedBy', '')
        upby = Teacher.objects.get(username=id)
        detail = request.POST.get('detail', '')
        if g_id == 1:
            return render(request, 'examDashboard.html')
        else:
            assignment = Assignment(assignment_fileUpload=fileurl, assignment_name=assign_name, assignment_date=doa, assignment_start_time=ast,
                                    assignment_end_time=aet, assignment_detail=detail, dept=dept, uploaded_by=upby, course=course)
            assignment.save()
            return HttpResponse("<script>setTimeout(function(){window.location.href='/exam/addAssignment/'},0000);</script>")
    return render(request, 'addAssignment.html', params)


def viewAssignment(request,assignid):
    img, id = fun(request)
    g = request.user.groups.all()
    g_id = Group.objects.get(name=g[0]).id
    id = request.user.username
    if g_id == 1:
        assign = Assignment.objects.filter(assignment_id=assignid)
        print(assign)
        name = assign[0].assignment_name
        date = assign[0].assignment_date
        st = assign[0].assignment_start_time
        et = assign[0].assignment_end_time
        detail = assign[0].assignment_detail
        fileUpload = assign[0].assignment_fileUpload
        dept = assign[0].dept
        uploadedBy = assign[0].uploaded_by_id
        cid = assign[0].course_id
    else:
        return render(request, 'examDashboard.html')
    params = {'name': name, 'date': date, 'st': st, 'et': et, 'detail': detail,
              'fileUpload': fileUpload, 'dept': dept, 'uploadedBy': uploadedBy, 'cid': cid}
    return render(request, 'viewAssignment.html', params)


def viewAllAssignment(request):
    assignments = Assignment.objects.all()
    params = {'assignments':assignments}
    return render(request, 'viewAllAssignment.html',params)

def addExam(request):
    img, id = fun(request)
    g = request.user.groups.all()
    g_id = Group.objects.get(name=g[0]).id
    id = request.user.username
    if g_id == 1:
        return render(request, 'examDashboard.html')
    else:
        teacher = Teacher.objects.filter(username=id)
        uploadedBy = teacher[0].firstname + ' ' + teacher[0].lastname
        courses = Courses.objects.all()
        departments = Department.objects.all()
    params = {'uploadedBy': uploadedBy,
              'courses': courses, 'departments': departments}
    if request.method == "POST" and request.FILES['exam_file']:
        qpaperfile = request.FILES['exam_file']
        fileurl = qpaperfile
        examName = request.POST.get('examName', '')
        doe = request.POST.get('doe', '')
        est = request.POST.get('est', '')
        eet = request.POST.get('eet', '')
        examtype = request.POST.get('examType', '')
        cname = request.POST.get('course', '')
        course = Courses.objects.get(course_name=cname)
        dept = request.POST.get('dept', '')
        uploadedBy = request.POST.get('uploadedBy', '')
        upby = Teacher.objects.get(username=id)
        detail = request.POST.get('detail', '')
        if g_id == 1:
            return render(request, 'examDashboard.html')
        else:
            exam = Exam(exam_fileUpload=fileurl, exam_name=examName, exam_type=examtype, exam_date=doe,
                        exam_start_time=est, exam_end_time=eet, exam_detail=detail, course=course, dept=dept, uploaded_by=upby)
            exam.save()
            return HttpResponse("<script>setTimeout(function(){window.location.href='/exam/addExam/'},0000);</script>")
    return render(request, 'addExam.html', params)


def viewExam(request):
    img, id = fun(request)
    g = request.user.groups.all()
    g_id = Group.objects.get(name=g[0]).id
    id = request.user.username
    if g_id == 1:
        exam = Exam.objects.filter(exam_id=1)
        name = exam[0].exam_name
        etype = exam[0].exam_type
        date = exam[0].exam_date
        st = exam[0].exam_start_time
        et = exam[0].exam_end_time
        detail = exam[0].exam_detail
        fileUpload = exam[0].exam_fileUpload
        dept = exam[0].dept
        uploadedBy = exam[0].uploaded_by_id
        cid = exam[0].course_id
    else:
        return render(request, 'examDashboard.html')
    params = {'name': name, 'etype': etype, 'date': date, 'st': st, 'et': et, 'detail': detail,
              'fileUpload': fileUpload, 'dept': dept, 'uploadedBy': uploadedBy, 'cid': cid}
    return render(request, 'viewExam.html', params)


def viewAllExam(request):
    return render(request, 'viewAllExam.html')
