from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from ocp_app.models import Student, Department, Teacher, Courses,Announcement, Forum
# Create your views here.
def home(request):
    return render(request,'login.html')



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
    return redirect(home)


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
            return redirect('/signup/')
        if firstname.isalpha() == False | lastname.isalpha() == False:
            messages.error(request, "Name must be alphabetical.")
            return redirect('/signup/')
       
        if password!=confirm_pass:
            messages.error(request, "Password does not match.")
            return redirect('/signup/')
        if len(password)<=8:
            messages.error(request, "Password should be greater than 8 characters.")
            return redirect('/signup/')

        myuser = User.objects.create_user(username,email,password)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.save()

        return render(request,'home.html')
