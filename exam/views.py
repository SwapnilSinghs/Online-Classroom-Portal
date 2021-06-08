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
        print(request.POST)
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


def viewAssignment(request):
    return render(request, 'viewAssignment.html')


def addExam(request):
    return render(request, 'addExam.html')
