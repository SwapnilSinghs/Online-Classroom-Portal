from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from ocp_app.models import Student, Department, Teacher, Courses,Announcement, Forum
# Create your views here.

def examDashboard(request):
    return render(request, 'examDashboard.html')


def addAssignment(request):
    return render(request, 'addAssignment.html')

def addExam(request):
    return render(request, 'addExam.html')